import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="crud_app",
    user="ricardo",
    password="tomzy2219"
)
cursor = conn.cursor()

# 2. Cria a nova tabela com SERIAL (gera o ID 1, 2, 3... sozinho)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public."AGENDA_DE_CONTATOS" 
    (
        id SERIAL PRIMARY KEY,
        nome text NOT NULL,
        telefone CHAR(12) NOT NULL
    )
    TABLESPACE pg_default;
    ALTER TABLE public."AGENDA_DE_CONTATOS"
    OWNER to "ricardo"
""")

conn.commit()
cursor.close()
conn.close()

print("Nova tabela criada com sucesso! O ID é gerado automaticamente.")