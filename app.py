import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os


st.set_page_config(page_title="Sistema de Armários de Praia", layout="wide")

DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://neondb_owner:npg_TQRa1SWw5KlN@ep-soft-dew-aeznnvvq-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require")

@st.cache_resource
def get_engine():
    return create_engine(DB_URL)

@st.cache_data
def carregar_tabela(tabela):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            query = text(f"SELECT * FROM {tabela}")
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar {tabela}: {e}")
        return pd.DataFrame()


# Sidebar
st.sidebar.title("📂 Navegação")
opcao = st.sidebar.radio(
    "Selecione uma tabela:",
    ["Usuário", "Praia", "Armário", "Funcionário", "Cartão de Crédito", "Aluguel", "Pagamento", "Multa", "Notificação", "Avaliação", "Manutenção"]
)

tabela_map = {
    "Usuário": "usuario",
    "Praia": "praia",
    "Armário": "armario",
    "Funcionário": "funcionario",
    "Cartão de Crédito": "cartao_credito",
    "Aluguel": "aluguel",
    "Pagamento": "pagamento",
    "Multa": "multa",
    "Notificação": "notificacao",
    "Avaliação": "avaliacao",
    "Manutenção": "manutencao",
}

tabela_escolhida = tabela_map[opcao]
df = carregar_tabela(tabela_escolhida)
df = df.applymap(lambda x: str(x).strip().replace("'", "") if isinstance(x, str) else x)

st.title(f"📊 Dados da Tabela: {opcao}")

if not df.empty:
    with st.expander("🔍 Filtrar dados"):
        colunas = st.multiselect("Selecione colunas para filtrar", df.columns)
        filtros = {}
        for col in colunas:
            valor = st.text_input(f"Filtro para '{col}'")
            if valor:
                filtros[col] = valor

        if filtros:
            for col, val in filtros.items():
                df = df[df[col].astype(str).str.contains(val, case=False, na=False)]

    st.dataframe(df, use_container_width=True)

else:
    st.warning(f"Nenhum dado encontrado na tabela '{tabela_escolhida}'.")


if not df.empty:
    st.markdown("---")
    st.subheader("📈 Estatísticas Rápidas")
    st.write(f"**Total de registros:** {len(df)}")

    if tabela_escolhida == "notificacao" and not df.empty:
        st.write(f"**Total de notificações enviadas:** {len(df)}")

    if "valor" in df.columns:
        st.metric("💰 Soma total de valores", f"R$ {df['valor'].sum():.2f}")


if tabela_escolhida == "praia" and not df.empty:
    if "cidade" in df.columns:
        cidades = df["cidade"].value_counts().head(5)
        st.write("**Top 5 Cidades:**")
        st.write(cidades)

if tabela_escolhida == "aluguel" and not df.empty:
    st.markdown("---")
    st.subheader("📊 Resumo de Aluguéis por Usuário")
    st.write(df.groupby("usuario_id")["id"].count().reset_index(name="total_alugueis").sort_values(by="total_alugueis", ascending=False).head(10))

if tabela_escolhida == "notificacao" and not df.empty:
    st.markdown("---")
    st.subheader("📬 Número de notificações lidas")
    if "lida" in df.columns:
        lidas = df["lida"].eq(True).sum()
        st.write(f"Notificações lidas: **{lidas}**")


if tabela_escolhida == "avaliacao" and not df.empty:
    st.markdown("---")
    st.subheader("Média de Avaliações armários")
    if "nota" in df.columns:
        media_notas = df["nota"].mean()
        st.write(f"A média das avaliações é: **{media_notas:.2f}**")
