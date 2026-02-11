# ============================================================
# APP STREAMLIT — ANÁLISE DE VIBRAÇÕES E MANUTENÇÃO PREDITIVA
# ============================================================

# ----------------------------
# IMPORTS
# ----------------------------
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------
st.set_page_config(
    page_title="Análise de Vibração",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_features():
    """
    Carrega o arquivo Parquet contendo as features de vibração,
    estados operacionais e clusters.
    """
    return pd.read_parquet(
        "C:/Users/leona/Desktop/01 - Projeto Python/Analise_de_Vibracoes/parquet/features.parquet"
    )

features_df = load_features()

# Validação defensiva do carregamento
if features_df is None or features_df.empty:
    st.error("Erro ao carregar os dados. O arquivo Parquet está vazio ou não foi encontrado.")
    st.stop()

# ============================================================
# SIDEBAR — FILTROS
# ============================================================

st.sidebar.title("Filtros")

# Seleção do motor (origem do sinal)
motor_options = features_df["source_file"].dropna().unique()

motor = st.sidebar.selectbox(
    "Selecione o motor",
    motor_options
)

# Seleção de clusters (remove NaN)
cluster_options = (
    features_df["cluster_hdbscan"]
    .dropna()
    .unique()
)

cluster = st.sidebar.multiselect(
    "Selecione clusters",
    cluster_options,
    default=cluster_options
)

# ============================================================
# FILTRAGEM DO DATAFRAME
# ============================================================

df_filt = features_df[
    (features_df["source_file"] == motor) &
    (features_df["cluster_hdbscan"].isin(cluster))
]

# Remove linhas sem valores essenciais
df_filt = df_filt.dropna(subset=["RMS_total", "window_start"])

# Validação após filtros
if df_filt.empty:
    st.warning("Nenhum dado válido disponível para os filtros selecionados.")
    st.stop()

# Ordenação temporal (fundamental para gráficos de linha)
df_filt = df_filt.sort_values("window_start")

# ============================================================
# TÍTULO PRINCIPAL
# ============================================================

st.title("📈 Dashboard de Vibração e Manutenção Preditiva")

# ============================================================
# KPIs
# ============================================================

st.subheader("Indicadores Principais")

rms_valid = df_filt["RMS_total"].dropna()

col1, col2, col3 = st.columns(3)

col1.metric(
    "RMS médio",
    round(rms_valid.mean(), 3) if len(rms_valid) > 0 else "—"
)

col2.metric(
    "Máx RMS",
    round(rms_valid.max(), 3) if len(rms_valid) > 0 else "—"
)

col3.metric(
    "Anomalias (%)",
    round(
        (df_filt["estado"] != "Normal").mean() * 100,
        2
    ) if "estado" in df_filt.columns else "—"
)

# ============================================================
# GRÁFICO PRINCIPAL — RMS AO LONGO DO TEMPO
# ============================================================

st.subheader("Evolução Temporal da Vibração")

fig, ax = plt.subplots(figsize=(12, 4))

sns.lineplot(
    data=df_filt,
    x="window_start",
    y="RMS_total",
    hue="estado" if "estado" in df_filt.columns else None,
    palette={
        "Normal": "green",
        "Atenção": "orange",
        "Alerta": "red"
    } if "estado" in df_filt.columns else None,
    ax=ax
)

# ----------------------------
# Escala Y segura (à prova de NaN)
# ----------------------------
if len(rms_valid) > 0:
    y_min = rms_valid.quantile(0.01)
    y_max = rms_valid.quantile(0.99)

    if not np.isfinite(y_min) or not np.isfinite(y_max) or y_min == y_max:
        y_min = rms_valid.min()
        y_max = rms_valid.max()
else:
    y_min, y_max = 0, 1

ax.set_ylim(y_min, y_max)

ax.set_title("Vibração RMS com Estados Operacionais")
ax.set_xlabel("Tempo")
ax.set_ylabel("RMS")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# ============================================================
# CLUSTERS NO ESPAÇO PCA
# ============================================================

st.subheader("Clusters no Espaço PCA")

# Remove NaN de PCA
df_pca = df_filt.dropna(subset=["pca1", "pca2"])

if df_pca.empty:
    st.warning("Dados insuficientes para visualização PCA.")
else:
    fig2, ax2 = plt.subplots(figsize=(6, 5))

    sns.scatterplot(
        data=df_pca,
        x="pca1",
        y="pca2",
        hue="cluster_hdbscan",
        palette="tab10",
        ax=ax2
    )

    # Escala PCA segura
    x_min, x_max = df_pca["pca1"].quantile(0.01), df_pca["pca1"].quantile(0.99)
    y_min, y_max = df_pca["pca2"].quantile(0.01), df_pca["pca2"].quantile(0.99)

    if np.isfinite(x_min) and np.isfinite(x_max):
        ax2.set_xlim(x_min, x_max)
    if np.isfinite(y_min) and np.isfinite(y_max):
        ax2.set_ylim(y_min, y_max)

    ax2.set_title("Distribuição dos Clusters (PCA)")
    ax2.set_xlabel("PCA 1")
    ax2.set_ylabel("PCA 2")

    plt.tight_layout()
    st.pyplot(fig2)

# ============================================================
# TABELA DE DADOS (INSPEÇÃO)
# ============================================================

st.subheader("Amostra dos Dados Filtrados")

cols_show = [c for c in ["window_start", "RMS_total", "estado", "cluster_hdbscan"] if c in df_filt.columns]

st.dataframe(
    df_filt[cols_show].head(50),
    use_container_width=True
)

# ============================================================
# FOOTER
# ============================================================

st.caption("Projeto de Análise de Vibração • Manutenção Preditiva • Streamlit")