<h1 align="center">Patrick Fernandes Godinho Filho</h1>

<p align="center">
  <b>Analista de Dados · Cientista de Dados · Engenheiro de Dados</b><br>
  Python · SQL · ETL · DuckDB · Machine Learning
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/patrick-fernandes-godinho/"><img src="https://img.shields.io/badge/LinkedIn-1a1b27?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iJTIzNzBhNWZkIj48cGF0aCBkPSJNMjAuNDQ3IDIwLjQ1MmgtMy41NTR2LTUuNTY5YzAtMS4zMjgtLjAyNy0zLjAzNy0xLjg1Mi0zLjAzNy0xLjg1MyAwLTIuMTM2IDEuNDQ1LTIuMTM2IDIuOTM5djUuNjY3SDkuMzUxVjloMy40MTR2MS41NjFoLjA0NmMuNDc3LS45IDEuNjM3LTEuODUgMy4zNy0xLjg1IDMuNjAxIDAgNC4yNjcgMi4zNyA0LjI2NyA1LjQ1NXY2LjI4NnpNNS4zMzcgNy40MzNjLTEuMTQ0IDAtMi4wNjMtLjkyNi0yLjA2My0yLjA2NSAwLTEuMTM4LjkyLTIuMDYzIDIuMDYzLTIuMDYzIDEuMTQgMCAyLjA2NC45MjUgMi4wNjQgMi4wNjMgMCAxLjEzOS0uOTI1IDIuMDY1LTIuMDY0IDIuMDY1em0xLjc4MiAxMy4wMTlIMy41NTVWOWgzLjU2NHYxMS40NTJ6TTIyLjIyNSAwSDEuNzcxQy43OTIgMCAwIC43NzQgMCAxLjcyOXYyMC41NDJDMCAyMy4yMjcuNzkyIDI0IDEuNzcxIDI0aDIwLjQ1MUMyMy4yIDI0IDI0IDIzLjIyNyAyNCAyMi4yNzFWMS43MjlDMjQgLjc3NCAyMy4yIDAgMjIuMjI1IDB6Ii8+PC9zdmc+" alt="LinkedIn"></a>
  <a href="mailto:patrickfgf@gmail.com"><img src="https://img.shields.io/badge/patrickfgf%40gmail.com-1a1b27?style=flat-square&logo=gmail&logoColor=70a5fd" alt="E-mail: patrickfgf@gmail.com"></a>
</p>

<p align="center">Brasília-DF · remoto ou híbrido · CLT ou PJ</p>

---

Analista de Dados na área de Infraestrutura da **CNI** (Confederação Nacional da Indústria), com atuação ponta a ponta em **Análise, Engenharia e Ciência de Dados**: da coleta via APIs e fontes públicas ao ETL em Python e SQL, e daí a relatórios, dashboards e modelos que viram base de decisão. Construo pipelines com testes automatizados, CI/CD e controle de qualidade de dados.

Aberto a oportunidades em Dados (Análise, Engenharia ou Ciência), Backend e Full-Stack.

## Experiência

**Analista de Dados** · CNI, Confederação Nacional da Indústria (Infraestrutura)<br>
<sub>Brasília-DF · presencial · Atual</sub><br>
Automação da coleta e do tratamento de bases públicas de infraestrutura (energia elétrica, petróleo e combustíveis, telecomunicações, transportes e logística, rodovias, aviação, mineração e agropecuária), pipelines ETL com validação de esquema e execução idempotente, SQL (DuckDB) e Polars sobre Parquet e análises geoespaciais (DuckDB Spatial, Shapely). Estudos de priorização de investimentos em rodovias federais, auditoria de qualidade de dados contra fontes primárias (API SIDRA do IBGE) e geração automatizada de boletins, notas técnicas e relatórios em PDF.

**Desenvolvedor Full-Stack** · Caminho Canadá MD<br>
<sub>Remoto · 05/2026 – Atual</sub><br>
Desenvolvedor único do produto digital de um curso online para médicos: aplicação web em Astro e TypeScript no Cloudflare Pages, com captura de leads (validação, proteção anti-bot, LGPD), automação de métricas de marketing via APIs do GA4, da Meta e do Instagram com OAuth 2.0 e relatórios em Python, pipeline de transcrição das videoaulas e CI/CD com GitHub Actions.

**Engenheiro de Dados** · Eldorado Imobiliária<br>
<sub>Remoto · 01/2026 – 07/2026</sub><br>
Construí e mantive a estrutura de dados de uma imobiliária com mais de 25 anos de mercado em Brasília: pipeline event-driven em Python e FastAPI que recebia os leads dos portais por webhook, contratos de dados com Pydantic, DuckDB em camadas (raw → curated), deduplicação e entity resolution, lead scoring com roteamento ao CRM (Trello API) e dashboards em Streamlit, com Docker e deploy no Fly.io.

**Desenvolvedor Web** · clínica de ortopedia e traumatologia<br>
<sub>Remoto · 10/2025 – 12/2025</sub><br>
Site institucional em Astro e TypeScript no Cloudflare Pages (SEO técnico, GA4 condicionado a consentimento, adequação à LGPD) e automação em Python que extraía dados de documentos escaneados e gerava o relatório antes compilado à mão.

## Projetos

### Rio Airbnb Pricing Lab
[Demo ao vivo](https://rio-airbnb-pricing-lab-project.streamlit.app/) · [Documentação](https://patrickfgf.github.io/rio-airbnb-pricing-lab/) · [Código](https://github.com/Patrickfgf/rio-airbnb-pricing-lab)

Recomenda uma faixa de preço para anfitriões do Airbnb no Rio de Janeiro, com dados abertos do Inside Airbnb. Combina regressão hedônica com efeitos fixos de bairro e comparação com anúncios semelhantes, sobre um pipeline reprodutível DuckDB → Parquet com contratos de dados (pandera), testes automatizados, CI e dashboard em Streamlit.

O objetivo original, maximizar RevPAN, se mostrou **não identificável** nos dados: documentei o diagnóstico e re-escopei o produto para posicionamento de preço.

### Real Estate Lead Pipeline
[Demo ao vivo](https://real-estate-lead-pipeline-7jjxw8u3fnlwrzk63prwxq.streamlit.app/) · [Código](https://github.com/Patrickfgf/real-estate-lead-pipeline)

Versão pública e anonimizada, com dados sintéticos, do pipeline de leads que construí na Eldorado Imobiliária: webhooks em FastAPI, validação com Pydantic e fila de revisão para payloads inválidos, deduplicação e entity resolution, camadas raw → curated em DuckDB, lead scoring, criação automática do card no Trello e dashboard de funil em Streamlit. Docker, testes automatizados e CI.

### TripOptimizer
[Demo ao vivo](https://tripoptimizer-rouge.vercel.app) · código privado<br>
<sub>A API hiberna quando fica ociosa: o primeiro acesso pode levar de 30 a 60 s.</sub>

Encontra a ordem de visita mais barata para uma viagem de avião por várias cidades, dentro de uma janela de datas flexível. Modelado como problema do caixeiro viajante (TSP) com custo dependente da data; o repositório implementa o algoritmo exato Held-Karp (programação dinâmica), validado contra força bruta como oráculo de teste. Tarifas reais via API com cache em PostgreSQL, FastAPI e React com TypeScript, testes automatizados no back-end e no front-end, CI/CD e deploy em Render e Vercel.

Nasceu do meu intercâmbio em Coimbra, quando viajei por 15 países.

### Weather Trend Forecasting
[Código](https://github.com/Patrickfgf/weather-trend-forecasting)

Previsão de temperatura diária por cidade, 7 dias à frente, sobre o Global Weather Repository (Kaggle), com backtest temporal sem vazamento de dados. Compara modelos estatísticos por cidade (SARIMAX, Holt-Winters) com um modelo global em painel (XGBoost, LightGBM) e os combina em ensemble; inclui detecção de anomalias (Isolation Forest, LOF, STL), explicabilidade com SHAP e testes que barram vazamento.

## Como eu trabalho

- Contratos de dados na entrada (Pydantic, pandera) e pipelines idempotentes em camadas, do dado cru ao curado.
- Parquet como formato intermediário; DuckDB e Polars quando o volume pede.
- Testes automatizados e CI como parte da entrega; em modelagem, validação temporal sem vazamento e baseline simples antes do modelo complexo.
- IA como alavanca de engenharia: desenvolvo com Claude Code como par de programação e aplico LLMs à automação de processos.

## Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-1a1b27?style=flat-square&logo=python&logoColor=70a5fd" alt="Python">
  <img src="https://img.shields.io/badge/PostgreSQL-1a1b27?style=flat-square&logo=postgresql&logoColor=70a5fd" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/DuckDB-1a1b27?style=flat-square&logo=duckdb&logoColor=70a5fd" alt="DuckDB">
  <img src="https://img.shields.io/badge/Polars-1a1b27?style=flat-square&logo=polars&logoColor=70a5fd" alt="Polars">
  <img src="https://img.shields.io/badge/pandas-1a1b27?style=flat-square&logo=pandas&logoColor=70a5fd" alt="pandas">
  <img src="https://img.shields.io/badge/Parquet-1a1b27?style=flat-square&logo=apacheparquet&logoColor=70a5fd" alt="Parquet">
  <img src="https://img.shields.io/badge/FastAPI-1a1b27?style=flat-square&logo=fastapi&logoColor=70a5fd" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-1a1b27?style=flat-square&logo=docker&logoColor=70a5fd" alt="Docker">
  <img src="https://img.shields.io/badge/GitHub_Actions-1a1b27?style=flat-square&logo=githubactions&logoColor=70a5fd" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/scikit--learn-1a1b27?style=flat-square&logo=scikitlearn&logoColor=70a5fd" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Streamlit-1a1b27?style=flat-square&logo=streamlit&logoColor=70a5fd" alt="Streamlit">
</p>

- **Dados e análise:** Python (pandas, Polars, NumPy) · SQL · PostgreSQL · DuckDB · Parquet · Excel avançado · Power BI (PL-300 em preparação) · Streamlit · Plotly · matplotlib · seaborn
- **Engenharia de dados:** ETL/ELT em camadas (raw → curated) · webhooks e APIs REST (FastAPI) · integração de APIs com OAuth 2.0 · Pydantic · pandera · dados geoespaciais (DuckDB Spatial, Shapely) · Docker · GitHub Actions · pytest · Ruff · uv · Git
- **Ciência de dados e estatística:** scikit-learn · statsmodels · XGBoost · LightGBM · SHAP · séries temporais · regressão hedônica e econometria · detecção de anomalias
- **Web e cloud:** TypeScript · React · Astro · Cloudflare · Google Cloud (APIs) · Fly.io · Render · Vercel
- **Em estudo:** Airflow · AWS

## Formação e certificações

- **Economia**, IDP: último semestre, conclusão em 12/2026, ênfase quantitativa (econometria e estatística)
- **Engenharia de Software**, IDP: em andamento
- **Intercâmbio**, Universidade de Coimbra, Portugal (2025–2026)
- **Certificação:** Cambridge C1 Advanced (CAE, 2021) · **em preparação:** AWS Data Engineer Associate (DEA-C01), AWS Cloud Practitioner (CLF-C02) e Microsoft Power BI Data Analyst (PL-300)
- **Idiomas:** português nativo · inglês C1 · espanhol intermediário

<details>
<summary><b>English summary</b></summary>
<br>

Data Analyst on the Infrastructure team at CNI (Brazil's National Confederation of Industry), working end to end across data analysis, data engineering and data science: API and public-source ingestion, Python and SQL ETL pipelines (DuckDB, Polars, Parquet), statistical modeling and automated reporting, backed by automated tests and CI/CD. Previously Data Engineer at Eldorado Imobiliária, a real-estate agency in Brasília, where I built an event-driven lead pipeline with FastAPI and DuckDB. B.Sc. in Economics (final semester, quantitative track) and B.Sc. in Software Engineering (in progress) at IDP, with an exchange program at the University of Coimbra. English C1 (Cambridge CAE). Based in Brasília, open to Data, Backend and Full-Stack roles, remote or hybrid, as an employee or contractor.

Contact: patrickfgf@gmail.com · [LinkedIn](https://www.linkedin.com/in/patrick-fernandes-godinho/)

</details>

<details>
<summary><b>Atividade no GitHub</b> (inclui contribuições em repositórios privados)</summary>
<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/Patrickfgf/Patrickfgf/cards/stats.svg" alt="Estatísticas de contribuição no GitHub" width="44%">
  <img src="https://raw.githubusercontent.com/Patrickfgf/Patrickfgf/cards/streak.svg" alt="Sequência de contribuições no GitHub" width="52%">
</p>
<p align="center"><sub>Cards gerados diariamente por uma GitHub Action própria. Boa parte do meu trabalho fica em repositórios privados.</sub></p>
</details>

<p align="center">
  <img src="https://raw.githubusercontent.com/Patrickfgf/Patrickfgf/output/github-contribution-grid-snake-dark.svg" alt="Animação sobre o gráfico de contribuições no GitHub" width="100%">
</p>
