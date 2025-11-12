# popularBD.py — versão ajustada com correção de FK para armário
import os
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

EXCEL_PATH = r"C:\Users\User\Downloads\Trabalho_3_Planilha_Limpa.xlsx"

# === 1. Conexão ===
def get_engine():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise EnvironmentError("❌ A variável de ambiente DATABASE_URL não está definida.")
    return create_engine(DATABASE_URL, echo=False)

# === 2. Correção de IDs ===
def ajustar_ids(df, coluna_id, ids_validos):
    if coluna_id not in df.columns:
        return df

    if not ids_validos:
        print(f"⚠️ Nenhum ID válido encontrado para '{coluna_id}'. IDs não serão ajustados.")
        return df

    df[coluna_id] = df[coluna_id].apply(
        lambda x: x if x in ids_validos else max(ids_validos)
    )
    return df

# === 3. Leitura das abas ===
def load_sheets(path):
    xls = pd.ExcelFile(path)
    dfs = {}

    for sheet in xls.sheet_names:
        df_raw = pd.read_excel(path, sheet_name=sheet, header=None)

        header_row = None
        for i, row in df_raw.iterrows():
            if row.astype(str).str.contains("cpf|nome|email|telefone|cod|id", case=False).any():
                header_row = i
                break

        if header_row is None:
            print(f"⚠️ Nenhum cabeçalho detectado na aba '{sheet}'. Pulando.")
            continue

        df = pd.read_excel(path, sheet_name=sheet, header=header_row)

        df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed|query', case=False)]
        df = df.dropna(how="all").reset_index(drop=True)
        df.columns = [str(c).strip().lower() for c in df.columns]

        dfs[sheet.lower()] = df
        print(f"📄 Aba '{sheet}' carregada com {len(df)} linhas e {len(df.columns)} colunas.")

    return dfs

# === 4. População ===
def seed():
    if not os.path.exists(EXCEL_PATH):
        raise FileNotFoundError(f"❌ Planilha não encontrada: {EXCEL_PATH}")

    engine = get_engine()
    dfs = load_sheets(EXCEL_PATH)

    insp = inspect(engine)
    tabelas_existentes = insp.get_table_names()
    print("Tabelas encontradas:", tabelas_existentes)

    with engine.begin() as conn:

        # === Ordem correta de inserção (respeitando FKs) ===
        ordem = [
            "usuario",
            "praia",
            "armario",
            "funcionario",
            "cartao_credito",
            "aluguel",
            "pagamento",
            "multa",
            "notificacao",
            "avaliacao",
            "manutencao"
        ]

        # Insere cada tabela na ordem certa
        for tabela in ordem:
            if tabela not in dfs:
                continue

            if tabela not in tabelas_existentes:
                print(f"⚠️ Tabela '{tabela}' não existe no banco. Pulando.")
                continue

            df = dfs[tabela]

            try:
                df.to_sql(tabela, conn, if_exists='append', index=False)
                print(f"✅ {len(df)} registros inseridos em '{tabela}'")
            except SQLAlchemyError as e:
                print(f"⚠️ Erro ao inserir em '{tabela}': {e}")

    print("🎉 População concluída com sucesso!")

# === Execução ===
if __name__ == "__main__":
    seed()
