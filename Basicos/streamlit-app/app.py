import os
from datetime import datetime
import time
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Streamlit = Docker (prod-Ready)",
     page_icon="🐳",
    layout="wide",
)

APP_NAME=os.getenv("APP_NAME", "Streamlit Docker App")
ENV = os.getenv("APP_ENV", "production")
st.sidebar.title("⚙️ Configurações")
st.sidebar.write(f"**Aplicação:** {APP_NAME}")
st.sidebar.write(f"**Ambiente:** {ENV}")
st.sidebar.write(f"**Hora do servidor:** {datetime.utcnow():%Y-%m-%d %H:%M:%S} UTC")

st.title("🐳 Streamlit rodando dentro de um container Docker")
st.write(
    """
    Este exemplo :
    - Dependências pinadas
    - Usuário não-root
    - Healthcheck
    - Modo DEV via Docker Compose (hot-reload)
    """
)

st.header("1) Geração de dados e cache")
@st.cache_data(ttl=60)
def generate_data(rows: int = 5000) -> pd.DataFrame:
    time.sleep(0.5)  # simula custo de I/O
    x = np.random.randn(rows).cumsum()
    y = np.random.randn(rows).cumsum()
    return pd.DataFrame({"x": x, "y": y})

rows = st.slider("Quantidade de linhas", 1000, 20000, 5000, step=1000)
df = generate_data(rows)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Amostra dos dados")
    st.dataframe(df.head(10), use_container_width=True)
with col2:
    st.subheader("Gráfico (linha)")
    st.line_chart(df, use_container_width=True)

st.header("2) Upload de CSV")
uploaded = st.file_uploader("Envie um CSV para visualizar", type=["csv"])
if uploaded is not None:
    user_df = pd.read_csv(uploaded)
    st.success(f"Arquivo carregado: {uploaded.name} ({len(user_df)} linhas)")
    st.dataframe(user_df.head(50), use_container_width=True)

st.header("3) Saúde da aplicação")
st.info("Se esta página responde, o container provavelmente está saudável 😉")
