import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Sistema de Armários de Praia", layout="wide")

DB_URL = "postgresql+psycopg2://neondb_owner:npg_TQRa1SWw5KlN@ep-soft-dew-aeznnvvq-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(DB_URL)

@st.cache_data
def carregar_tabela(tabela):
    try:
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
    st.write(f"**Colunas disponíveis:** {', '.join(df.columns)}")

    if "valor" in df.columns:
        st.metric("💰 Soma total de valores", f"R$ {df['valor'].sum():.2f}")

if tabela_escolhida == "aluguel" and not df.empty:
    st.markdown("---")
    st.subheader("📊 Resumo de Aluguéis por Usuário")
    resumo = df.groupby("usuario_id")["valor"].sum().reset_index()
    st.bar_chart(resumo, x="usuario_id", y="valor")
