"""Generate static profile cards (stats, top languages, streak) as SVG files.

Why this exists: the public instances of github-readme-stats and streak-stats are
third-party services queried at page-load time. When they are slow or down, GitHub's
camo proxy returns 502/504 and caches the failure for hours, so the cards vanish from
the profile. Generating the SVGs in CI and committing them turns a request-time
dependency into a build-time one: visitors load a static file that always resolves.

Grain: one run = one snapshot of the account's public+private contribution state.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

GITHUB_GRAPHQL = "https://api.github.com/graphql"
STREAK_UPSTREAM = "https://streak-stats.demolab.com"

# tokyonight palette, matching the badges already used in the README
BG = "#1a1b27"
TITLE = "#70a5fd"
TEXT = "#38bdae"
ICON = "#bf91f3"
MUTED = "#565f89"

STREAK_RETRIES = 3
STREAK_TIMEOUT = 60  # generous: an 8s cold start is harmless in CI, fatal behind camo


class CardError(RuntimeError):
    """Raised when a card cannot be produced from live data."""


@dataclass(frozen=True)
class Stats:
    contributions: int
    commits: int
    pull_requests: int
    repositories: int
    followers: int
    private_share: float


def graphql(query: str, token: str, variables: dict | None = None) -> dict:
    """POST a GraphQL query, raising on transport or GraphQL-level errors."""
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    request = urllib.request.Request(
        GITHUB_GRAPHQL,
        data=payload,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-card-generator",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = json.loads(response.read())
    if "errors" in body:
        raise CardError(f"GraphQL returned errors: {body['errors']}")
    return body["data"]


def assert_sees_private_repos(login: str, token: str) -> None:
    """Fail loudly when the token cannot see the account's private repositories.

    contributionsCollection is public when the profile exposes private contributions,
    so commit counts come out right even with a scope-less token. Repository and
    language counts do not: they silently narrow to the public subset, producing a
    plausible number for the wrong universe. Better to keep the previous card than to
    publish "8 repositories" when there are 18.
    """
    counts = graphql(
        """
        query($login: String!) {
          user(login: $login) {
            all: repositories(ownerAffiliations: OWNER, isFork: false) { totalCount }
            private: repositories(ownerAffiliations: OWNER, isFork: false, privacy: PRIVATE) {
              totalCount
            }
          }
        }
        """,
        token,
        {"login": login},
    )["user"]
    if counts["private"]["totalCount"] == 0 and counts["all"]["totalCount"] > 0:
        raise CardError(
            "token cannot see private repositories -- set CARDS_TOKEN to a PAT with "
            "`repo` scope, or this card would describe the public subset only"
        )


def collect_stats(login: str, token: str) -> Stats:
    """Aggregate lifetime counters, including contributions in private repos."""
    assert_sees_private_repos(login, token)
    profile = graphql(
        """
        query($login: String!) {
          user(login: $login) {
            createdAt
            followers { totalCount }
            pullRequests(first: 1) { totalCount }
            repositories(first: 1, ownerAffiliations: OWNER, isFork: false) { totalCount }
          }
        }
        """,
        token,
        {"login": login},
    )["user"]

    first_year = int(profile["createdAt"][:4])
    current_year = time.gmtime().tm_year

    contributions = commits = private = 0
    for year in range(first_year, current_year + 1):
        window = graphql(
            """
            query($login: String!, $from: DateTime!, $to: DateTime!) {
              user(login: $login) {
                contributionsCollection(from: $from, to: $to) {
                  totalCommitContributions
                  restrictedContributionsCount
                  contributionCalendar { totalContributions }
                }
              }
            }
            """,
            token,
            {
                "login": login,
                "from": f"{year}-01-01T00:00:00Z",
                "to": f"{year}-12-31T23:59:59Z",
            },
        )["user"]["contributionsCollection"]
        contributions += window["contributionCalendar"]["totalContributions"]
        commits += window["totalCommitContributions"]
        private += window["restrictedContributionsCount"]

    total_commits = commits + private
    return Stats(
        contributions=contributions,
        commits=total_commits,
        pull_requests=profile["pullRequests"]["totalCount"],
        repositories=profile["repositories"]["totalCount"],
        followers=profile["followers"]["totalCount"],
        private_share=private / total_commits if total_commits else 0.0,
    )


def collect_languages(login: str, token: str, limit: int = 8) -> list[tuple[str, str, float]]:
    """Return [(name, colour, share)] by bytes across all owned non-fork repos."""
    assert_sees_private_repos(login, token)
    data = graphql(
        """
        query($login: String!) {
          user(login: $login) {
            repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
              nodes {
                languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
                  edges { size node { name color } }
                }
              }
            }
          }
        }
        """,
        token,
        {"login": login},
    )
    sizes: dict[str, int] = {}
    colours: dict[str, str] = {}
    for repo in data["user"]["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            sizes[name] = sizes.get(name, 0) + edge["size"]
            colours[name] = edge["node"]["color"] or MUTED
    if not sizes:
        raise CardError("no language data returned for this account")

    total = sum(sizes.values())
    ranked = sorted(sizes.items(), key=lambda kv: kv[1], reverse=True)[:limit]
    return [(name, colours[name], size / total) for name, size in ranked]


def fetch_streak(login: str) -> str:
    """Fetch the streak card upstream, retrying past its ~8s cold start.

    The upstream service is alive but slow on first hit. Retrying here is safe
    because CI has no timeout pressure, unlike GitHub's image proxy.
    """
    url = f"{STREAK_UPSTREAM}?user={login}&theme=tokyonight&hide_border=true"
    last_error: Exception | None = None
    for attempt in range(1, STREAK_RETRIES + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "profile-card-generator"})
            with urllib.request.urlopen(request, timeout=STREAK_TIMEOUT) as response:
                body = response.read().decode("utf-8", errors="replace")
            if "<svg" not in body:
                raise CardError("upstream response was not an SVG")
            return flatten_animations(body)
        except (urllib.error.URLError, CardError, TimeoutError) as error:
            last_error = error
            print(f"  streak attempt {attempt}/{STREAK_RETRIES} failed: {error}", file=sys.stderr)
            if attempt < STREAK_RETRIES:
                time.sleep(attempt * 5)
    raise CardError(f"streak upstream unreachable after {STREAK_RETRIES} attempts: {last_error}")


def flatten_animations(svg: str) -> str:
    """Apply the end state of the upstream fade-in animations statically.

    The upstream card hides 11 elements behind `opacity: 0` and reveals them with
    staggered CSS animations. That is fine for a live-rendered card, but a committed
    SVG must not depend on the renderer running CSS animation just to be legible:
    anything that rasterises the file without animating shows an empty card.
    Since every keyframe ends at `opacity: 1`, collapsing to that state is lossless.
    """
    flattened = re.sub(r"opacity:\s*0\s*;\s*animation:[^'\"]*", "opacity: 1", svg)
    flattened = re.sub(r"animation:\s*currstreak[^'\"]*", "", flattened)
    # Check the inline style attributes only. The <style> block keeps its @keyframes
    # (which legitimately contain "opacity: 0" at the 0% stop), so a naive substring
    # test on the whole document would always fire.
    hidden = re.findall(r"style='[^']*opacity:\s*0\s*[;']", flattened)
    if hidden:
        raise CardError(f"{len(hidden)} element(s) still hidden after flattening")
    return flattened


def _fmt(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def render_stats(stats: Stats, login: str) -> str:
    rows = [
        ("Contribuições", _fmt(stats.contributions)),
        ("Commits", _fmt(stats.commits)),
        ("Pull Requests", _fmt(stats.pull_requests)),
        ("Repositórios", _fmt(stats.repositories)),
        ("Seguidores", _fmt(stats.followers)),
    ]
    width, height = 420, 195
    lines = []
    for index, (label, value) in enumerate(rows):
        y = 74 + index * 21
        lines.append(
            f'<circle cx="34" cy="{y - 4}" r="3.5" fill="{ICON}"/>'
            f'<text x="50" y="{y}" class="label">{label}</text>'
            f'<text x="{width - 25}" y="{y}" class="value" text-anchor="end">{value}</text>'
        )
    private_note = f"{stats.private_share:.0%} em repositórios privados"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" \
viewBox="0 0 {width} {height}" role="img" aria-label="Estatísticas de {login}">
  <style>
    .title {{ font: 600 18px 'Segoe UI', Ubuntu, sans-serif; fill: {TITLE}; }}
    .label {{ font: 400 14px 'Segoe UI', Ubuntu, sans-serif; fill: {TEXT}; }}
    .value {{ font: 600 14px 'Segoe UI', Ubuntu, sans-serif; fill: {TEXT}; }}
    .note  {{ font: 400 11px 'Segoe UI', Ubuntu, sans-serif; fill: {MUTED}; }}
  </style>
  <rect width="{width}" height="{height}" rx="6" fill="{BG}"/>
  <text x="25" y="40" class="title">Estatísticas de {login}</text>
  {"".join(lines)}
  <text x="25" y="{height - 16}" class="note">{private_note} &#183; atualizado diariamente</text>
</svg>"""


def render_languages(languages: list[tuple[str, str, float]]) -> str:
    width = 350
    height = 195
    bar_y, bar_w, bar_h = 55, width - 50, 8

    segments, offset = [], 0.0
    for _, colour, share in languages:
        seg_w = share * bar_w
        segments.append(
            f'<rect x="{25 + offset:.2f}" y="{bar_y}" width="{seg_w:.2f}" '
            f'height="{bar_h}" fill="{colour}"/>'
        )
        offset += seg_w

    legend = []
    for index, (name, colour, share) in enumerate(languages):
        column, row = index % 2, index // 2
        x = 25 + column * 160
        y = 95 + row * 22
        legend.append(
            f'<circle cx="{x + 5}" cy="{y - 4}" r="5" fill="{colour}"/>'
            f'<text x="{x + 18}" y="{y}" class="label">{name} {share:.1%}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" \
viewBox="0 0 {width} {height}" role="img" aria-label="Linguagens mais usadas">
  <style>
    .title {{ font: 600 18px 'Segoe UI', Ubuntu, sans-serif; fill: {TITLE}; }}
    .label {{ font: 400 12px 'Segoe UI', Ubuntu, sans-serif; fill: {TEXT}; }}
  </style>
  <rect width="{width}" height="{height}" rx="6" fill="{BG}"/>
  <text x="25" y="35" class="title">Linguagens mais usadas</text>
  <clipPath id="round"><rect x="25" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="4"/></clipPath>
  <g clip-path="url(#round)">
    <rect x="25" y="{bar_y}" width="{bar_w}" height="{bar_h}" fill="{MUTED}"/>
    {"".join(segments)}
  </g>
  {"".join(legend)}
</svg>"""


def main() -> int:
    token = os.environ.get("CARDS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("ERROR: set CARDS_TOKEN (or GITHUB_TOKEN) in the environment", file=sys.stderr)
        return 1
    login = os.environ.get("CARDS_LOGIN", "Patrickfgf")
    out_dir = Path(os.environ.get("CARDS_OUT", "dist"))
    out_dir.mkdir(parents=True, exist_ok=True)

    # Each card is independent: one failing upstream must not blank the others.
    # A card that cannot be regenerated keeps whatever version is already committed.
    failures = []
    for name, build in (
        ("stats.svg", lambda: render_stats(collect_stats(login, token), login)),
        ("top-langs.svg", lambda: render_languages(collect_languages(login, token))),
        ("streak.svg", lambda: fetch_streak(login)),
    ):
        try:
            (out_dir / name).write_text(build(), encoding="utf-8")
            print(f"  wrote {out_dir / name}")
        except Exception as error:  # noqa: BLE001 - report and continue to next card
            failures.append(f"{name}: {error}")
            print(f"  FAILED {name}: {error}", file=sys.stderr)

    if len(failures) == 3:
        print("ERROR: every card failed to generate", file=sys.stderr)
        return 1
    if failures:
        print(f"WARNING: {len(failures)} card(s) kept their previous version", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
