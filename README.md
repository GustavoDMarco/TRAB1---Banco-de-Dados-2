🏖️ Sistema de Armários de Praia – Dashboard & População de Banco
Aplicação desenvolvida para visualização, filtragem e análise das tabelas de um banco PostgreSQL, além de script automatizado para popular o banco a partir de planilhas Excel.

🚀 DEPLOY:
https://trankaki.streamlit.app/

🔹 Back-end / Banco de Dados
PostgreSQL (Neon DB)
SQLAlchemy
Pandas
Scripts de popular tabelas (.xlsx → banco)

🔹 Front-end / Dashboard
Streamlit
Pandas
Python 3.10+

🗂️ Principais Arquivos:
├── popularBD.py        # Script de leitura de Excel + inserção ordenada no banco
├── APP.py              # Dashboard Streamlit para visualização das tabelas

⚙️ Configuração do Banco & Scripts
1️⃣ Variável de ambiente (OBRIGATÓRIO)

Crie um arquivo .env na raiz:
DATABASE_URL=postgresql+psycopg2://usuario:senha@host/banco?sslmode=require

🧩 Script de População – popularBD.py
Esse script:

✔️ Lê automaticamente todas as abas da planilha
✔️ Detecta a linha de cabeçalho
✔️ Limpa colunas indesejadas
✔️ Ajusta IDs quando necessário
✔️ Insere no banco respeitando a ordem das FKs
✔️ Ignora tabelas inexistentes

▶️ Executar o script
python popularBD.py
O script exibirá:

Tabelas detectadas
Quantidade de registros inseridos por aba
Alertas de erros ou colunas ignoradas

📊 Dashboard – APP.py

Aplicação Web criada com Streamlit, permitindo:

✔️ Selecionar qualquer tabela
✔️ Visualizar dados formatados
✔️ Filtrar por colunas
✔️ Ocultar automaticamente dados sensíveis (senha, cvv)
✔️ Exibir estatísticas inteligentes por tabela
✔️ Contagem por status (armários, pagamentos, avaliações etc.)

A barra lateral permite navegar entre:
Usuário
Praia
Armário
Funcionário
Cartão de Crédito
Aluguel
Pagamento
Multa
Notificação
Avaliação
Manutenção

▶️ Executar o Dashboard
streamlit run APP.py

🧭 Funcionalidades do Dashboard
📌 Ocultação automática de informações sensíveis

Colunas como senha e cvv são removidas antes da exibição.

🔍 Filtros interativos

Permite buscar valores em qualquer coluna selecionada.

📈 Estatísticas por tabela:

Notificação: total e total de lidas

Armário: quantidade por status

Pagamento: concluídos, abertos e atrasados

Avaliação: média das notas

Aluguel: ranking por usuários

📝 Exemplo de interface

Tabelas exibidas com st.dataframe()

Filtros expansíveis

Métricas rápidas com st.metric()

Contagens automáticas

🗃️ Organização Interna do Código
🔹 popularBD.py

get_engine() → Conexão pelo env

load_sheets() → Lê planilhas dinamicamente

ajustar_ids() → Ajusta IDs inválidos

seed() → Insere todas as tabelas ordenadamente

🔹 APP.py

Cache para engine & carregamento de tabela

Ocultação de colunas sensíveis

Mapeamento de nomes para tabelas reais

Estatísticas específicas por tabela

