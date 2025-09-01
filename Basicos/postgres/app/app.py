import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import pandas as pd
import streamlit as st

DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "senha")
DB_NAME = os.getenv("POSTGRES_DB", "meubanco")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True)

def wait_for_db(retries=12, delay=2):
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except OperationalError as e:
            st.sidebar.warning(f"DB não disponível ainda (tentativa {attempt}/{retries})...")
            time.sleep(delay)
    raise RuntimeError("Não foi possível conectar ao banco de dados após várias tentativas.")

wait_for_db()

st.set_page_config(page_title="Streamlit + Postgres", layout="wide")
st.title("📦 Streamlit + Postgres (Docker) — Demo CRUD 'notes'")

st.sidebar.header("Conexão")
st.sidebar.write(f"{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
try:
    with engine.connect() as conn:
        v = conn.execute(text("SELECT now() as now")).mappings().first()
        st.sidebar.success(f"Conectado — {v['now']}")
except Exception as e:
    st.sidebar.error(f"Erro: {e}")

def list_tables():
    q = text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    with engine.connect() as conn:
        rows = conn.execute(q).mappings().all()
    return [r['table_name'] for r in rows]

tables = list_tables()
st.subheader("Tabelas encontradas")
st.write(tables)

st.header("Notas (tabela 'notes')")
if "notes" in tables:
    df = pd.read_sql("SELECT * FROM notes ORDER BY created_at DESC LIMIT 200", engine)
    st.dataframe(df, use_container_width=True)

    with st.expander("Criar nova nota"):
        title = st.text_input("Título")
        content = st.text_area("Conteúdo")
        if st.button("Salvar nova nota"):
            if not title or not content:
                st.error("Título e conteúdo são obrigatórios")
            else:
                with engine.begin() as conn:
                    conn.execute(
                        text("INSERT INTO notes (title, content) VALUES (:t, :c)"),
                        {"t": title, "c": content}
                    )
                st.success("Nota criada ✅")
                st.rerun()

    
    if not df.empty:
        selected_id = st.selectbox("Selecionar nota para editar/excluir", df["id"].tolist())
        if selected_id:
            row = df[df["id"] == selected_id].iloc[0]
            new_title = st.text_input("Editar título", value=row["title"], key="edit_title")
            new_content = st.text_area("Editar conteúdo", value=row["content"], key="edit_content")
            c1, c2 = st.columns(2)
            if c1.button("Salvar alterações"):
                with engine.begin() as conn:
                    conn.execute(
                        text("UPDATE notes SET title=:t, content=:c WHERE id=:id"),
                        {"t": new_title, "c": new_content, "id": int(selected_id)}
                    )
                st.success("Atualizado ✅")
                st.rerun()
            if c2.button("Excluir nota"):
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM notes WHERE id=:id"), {"id": int(selected_id)})
                st.success("Excluído ✅")
                st.rerun()
else:
    st.info("Tabela 'notes' não encontrada. Verifique se os scripts em db/init foram aplicados.")


st.header("Consulta SQL (apenas SELECT)")
sql = st.text_area("SQL (apenas SELECT permitido)", height=140)
if st.button("Executar consulta"):
    if sql.strip().lower().startswith("select"):
        try:
            df_sql = pd.read_sql(sql, engine)
            st.dataframe(df_sql, use_container_width=True)
        except Exception as e:
            st.error(f"Erro na query: {e}")
    else:
        st.warning("Somente consultas SELECT são permitidas aqui (evita alterações acidentais).")
