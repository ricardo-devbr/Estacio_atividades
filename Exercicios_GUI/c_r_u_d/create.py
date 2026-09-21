import psycopg2 

conn = psycopg2.connect(
    host = 'localhost',
    database = 'postgresDB',
    user = 'ricardo',
    password = 'tomzy2219'    
)
print('conectado com sucesso!')

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS public. "AGENDA"
(
    id integer PRIMARY KEY,
    nome text COLLATE pg_catalog."default" NOT NULL,
    telefone char(12) COLLATE pg_catalog. "default" NOT NULL
)
TABLESPACE pg_default;
ALTER TABLE public. "AGENDA"
    OWNER to "ricardo"
""")
cursor.execute('TRUNCATE TABLE public. "AGENDA";')
# INSERIR DADOS NA TABELA
cursor.execute(
    """
    INSERT INTO public. "AGENDA" (id, nome, telefone)
    VALUES (1, 'ricardo', '48988762739')
    """
)
cursor.execute(
    """
    INSERT INTO public. "AGENDA" (id, nome, telefone)
    VALUES (2, 'eduarda', '48988328472')
    """
)
# SALVAR ALTERACOES
conn.commit()

# LER DADOS
cursor.execute("""
    SELECT id, nome, telefone FROM public. "AGENDA";
"""
)
rows = cursor.fetchall()
for row in rows:
  print(f'ID: {row[0]}, Nome: {row[1]}, Telefone: {row[2]}')

cursor.close()
conn.close()