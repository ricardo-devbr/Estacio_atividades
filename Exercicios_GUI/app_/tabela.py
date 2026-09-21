import psycopg2

conexao = psycopg2.connect(
    dbname="postgresDB",
    user="ricardo",
    password="tomzy2219",
    host="localhost",
    port="5432"
)
print("Conexão com o banco de dados estabelecida com sucesso!")

cursor = conexao.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS tabela_de_dados (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco FLOAT NOT NULL
)
""")
conexao.commit()
print("Tabela criada com sucesso!")