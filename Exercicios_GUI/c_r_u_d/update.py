import psycopg2 

conn = psycopg2.connect(
    host = 'localhost',
    database = 'postgresDB',
    user = 'ricardo',
    password = 'tomzy2219'    
)
cursor = conn.cursor()
print('conectado com sucesso!')

cursor.execute(
    """
    UPDATE public. "AGENDA"
    SET nome = 'almeida'
    WHERE id = 1;
    """
)
conn.commit()

cursor.execute("""
SELECT id, nome, telefone FROM public."AGENDA";
""")
rows = cursor.fetchall()
for row in rows:
    print(f'ID: {row[0]}, Nome: {row[1]}, Telefone: {row[2]}')

cursor.close()
conn.close()