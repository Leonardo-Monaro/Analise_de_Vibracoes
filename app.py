import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# ============================================================
# CACHE
# ============================================================

@st.cache_data
def load_features():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "parquet", "features.parquet")
    return pd.read_parquet(file_path)

features_df = load_features()

# ============================================================
# NORMALIZAÇÃO (CORREÇÃO DEFINITIVA DOS FILTROS)
# ============================================================

if "cluster_hdbscan" in features_df.columns:
    features_df["cluster_hdbscan"] = (
        pd.to_numeric(features_df["cluster_hdbscan"], errors="coerce")
        .fillna(-1)
        .astype(int)
    )

if "cluster_kmeans" in features_df.columns:
    features_df["cluster_kmeans"] = (
        pd.to_numeric(features_df["cluster_kmeans"], errors="coerce")
        .fillna(-1)
        .astype(int)
    )

if "window_start" in features_df.columns:
    features_df["window_start"] = pd.to_datetime(
        features_df["window_start"], errors="coerce"
    )

# ============================================================
# SIDEBAR FILTROS
# ============================================================

st.sidebar.header("Filtros")

# Motor
if "source_file" in features_df.columns:
    motor_options = sorted(features_df["source_file"].dropna().unique())

    if len(motor_options) > 1:
        motor = st.sidebar.selectbox("Selecione o motor", motor_options)
        df_filt = features_df[features_df["source_file"] == motor]
    else:
        # Se só existe um motor, não filtra
        motor = motor_options[0]
        df_filt = features_df.copy()
else:
    df_filt = features_df.copy()

# Clusters
cluster_options = sorted(
    features_df["cluster_hdbscan"].dropna().unique()
)

cluster = st.sidebar.multiselect(
    "Selecione clusters",
    cluster_options,
    default=cluster_options
)

# Aplicando filtros
df_filt = features_df.copy()


if cluster:
    df_filt = df_filt[
        df_filt["cluster_hdbscan"].isin(cluster)
    ]

df_filt = df_filt.dropna(subset=["RMS_total", "window_start"])

if df_filt.empty:
    st.warning("Nenhum dado disponível com os filtros selecionados.")
    st.stop()

# ============================================================
# GRÁFICO RMS
# ============================================================

st.subheader("Evolução Temporal da Vibração")

fig_rms, ax_rms = plt.subplots(figsize=(10, 4))

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
    ax=ax_rms
)

rms_valid = df_filt["RMS_total"].dropna()

if len(rms_valid) > 0:
    y_min = rms_valid.quantile(0.01)
    y_max = rms_valid.quantile(0.99)
else:
    y_min, y_max = 0, 1

ax_rms.set_ylim(y_min, y_max)
ax_rms.set_title("Vibração RMS com Estados Operacionais")
ax_rms.set_xlabel("Tempo")
ax_rms.set_ylabel("RMS")

plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig_rms)

# ============================================================
# PCA CLUSTERS (HDBSCAN)
# ============================================================

st.subheader("Clusters no Espaço PCA")

df_pca = df_filt.dropna(subset=["pca1", "pca2"])

if not df_pca.empty:
    fig_pca, ax_pca = plt.subplots(figsize=(6, 4))

    sns.scatterplot(
        data=df_pca,
        x="pca1",
        y="pca2",
        hue="cluster_hdbscan",
        palette="tab10",
        s=40,
        ax=ax_pca
    )

    ax_pca.set_title("Distribuição dos Clusters (HDBSCAN)")
    ax_pca.set_xlabel("PCA 1")
    ax_pca.set_ylabel("PCA 2")

    plt.tight_layout()
    st.pyplot(fig_pca)
else:
    st.warning("Dados insuficientes para visualização PCA.")

# ============================================================
# COMPARAÇÃO KMEANS vs HDBSCAN (COMPACTO)
# ============================================================

st.subheader("Comparação entre Métodos de Clusterização")

fig_comp, axes = plt.subplots(1, 2, figsize=(12, 4))

sns.scatterplot(
    data=df_pca,
    x="pca1",
    y="pca2",
    hue="cluster_kmeans",
    palette="tab10",
    s=30,
    ax=axes[0]
)
axes[0].set_title("KMeans")

sns.scatterplot(
    data=df_pca,
    x="pca1",
    y="pca2",
    hue="cluster_hdbscan",
    palette="tab10",
    s=30,
    ax=axes[1]
)
axes[1].set_title("HDBSCAN")

plt.tight_layout()
st.pyplot(fig_comp)

# ============================================================
# VISUALIZAÇÃO HDBSCAN + ANOMALIAS (AGRUPADO)
# ============================================================

st.subheader("Clusters HDBSCAN + Possíveis Anomalias")

cluster_sizes = df_filt["cluster_hdbscan"].value_counts()
small_clusters = cluster_sizes[
    cluster_sizes < 0.05 * len(df_filt)
].index

anomalies = df_filt[
    df_filt["cluster_hdbscan"].isin(small_clusters)
]

fig_anom, axes_anom = plt.subplots(1, 2, figsize=(12, 4))

# Scatter PCA
sns.scatterplot(
    data=df_pca,
    x="pca1",
    y="pca2",
    hue="cluster_hdbscan",
    palette="tab10",
    s=40,
    ax=axes_anom[0]
)
axes_anom[0].set_title("Clusters HDBSCAN (PCA)")

# Série temporal com anomalias
axes_anom[1].plot(
    df_filt["window_start"],
    df_filt["RMS_total"],
    alpha=0.3
)

axes_anom[1].scatter(
    anomalies["window_start"],
    anomalies["RMS_total"],
    color="red",
    s=20,
    label="Possível anomalia"
)

axes_anom[1].legend()
axes_anom[1].set_title("Possíveis Anomalias no Tempo")

plt.tight_layout()
st.pyplot(fig_anom)