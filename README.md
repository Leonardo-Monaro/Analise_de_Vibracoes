# Análise de Vibrações

![GitHub repo size](https://img.shields.io/github/repo-size/Leonardo-Monaro/Analise_de_Vibracoes?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/Leonardo-Monaro/Analise_de_Vibracoes?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/Leonardo-Monaro/Analise_de_Vibracoes?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/Leonardo-Monaro/Analise_de_Vibracoes?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/Leonardo-Monaro/Analise_de_Vibracoes?style=for-the-badge)

<div display="inline">
&nbsp;&nbsp;<img width=100 src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original-wordmark.svg" />&nbsp;&nbsp;
&nbsp;&nbsp;<img width=100 src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/scikitlearn/scikitlearn-original.svg" />&nbsp;&nbsp;
&nbsp;&nbsp;<img width=100 src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pandas/pandas-original-wordmark.svg" />&nbsp;&nbsp;
  <img width=100 src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-plain-wordmark.svg" />
<div>
Análise de Vibração e Manutenção Preditiva

Este projeto tem como objetivo desenvolver uma pipeline completa de análise de vibração aplicada à manutenção preditiva, integrando engenharia de features, redução de dimensionalidade, clustering não supervisionado e visualização interativa via Streamlit.

O foco principal é detectar comportamentos anômalos em sinais de vibração, permitindo identificar padrões operacionais normais e desvios que podem indicar falhas incipientes em motores ou equipamentos rotativos.

🔍 Visão Geral do Processo

O fluxo do projeto é composto pelas seguintes etapas:

Leitura e pré-processamento dos sinais de vibração

Extração de features no domínio do tempo

RMS

Kurtosis

Estatísticas descritivas por janela

Normalização e tratamento de valores ausentes

Redução de dimensionalidade com PCA

Clusterização não supervisionada

KMeans

HDBSCAN

Classificação de estados operacionais

Normal

Atenção

Alerta

Persistência dos dados em formato Parquet

Visualização interativa via Streamlit

📊 Dashboard Interativo

O dashboard desenvolvido em Streamlit permite:

Filtrar dados por motor e cluster

Visualizar indicadores-chave (KPIs):

RMS médio

RMS máximo

Percentual de anomalias

Analisar a evolução temporal da vibração

Explorar a separação dos clusters no espaço PCA

Inspecionar os dados filtrados de forma tabular

O app foi desenvolvido com tratamento robusto de NaN, escalas seguras e validações defensivas, garantindo estabilidade mesmo com dados incompletos.

🧠 Técnicas Utilizadas

Python

Pandas / NumPy

Scikit-learn

HDBSCAN

Seaborn / Matplotlib

Streamlit

Parquet (armazenamento eficiente de dados)

🚀 Possíveis Evoluções

Definição dinâmica de limiares de alerta

Destaque automático de períodos anômalos

Integração com dados em tempo real

📌 Observação

Este projeto tem caráter educacional e experimental, mas foi estruturado seguindo boas práticas de engenharia de dados, análise exploratória e visualização, podendo servir como base para aplicações industriais reais.

▶️ Execução do Projeto
```bash
pip install -r requirements.txt
streamlit run app.py

Migração dos gráficos para Plotly

Deploy em nuvem
