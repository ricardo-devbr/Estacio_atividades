from tabela import conexao, cursor
from faker import Faker
from psycopg2 import Error

class AppBD:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect_to_db()

    def connect_to_db(self):
        self.conn = conexao
        self.cur = cursor
        print("Conexão com o banco de dados aberta com sucesso!")

    def selecionar_dados(self):
        try:
            self.cur.execute("""
                SELECT * FROM tabela_de_dados ORDER BY id
        """)
            registros = self.cur.fetchall()
            return registros
        except (Exception, Error) as erro:  
            print("Erro ao selecionar dados:", erro)
            return []
        
    def inserir_dados(self, nome, preco):
        try:
            self.cur.execute("""
            INSERT INTO tabela_de_dados (nome, preco)
            VALUES (%s, %s)""",
            (nome, preco)
        )
            self.conn.commit()
            print("\nDados inseridos com sucesso!\n")
        except (Exception, Error) as erro:
            print("Erro ao inserir dados:", erro)

    def atualizar_dados(self, id, nome, preco):
        try:
            self.cur.execute("""
            UPDATE tabela_de_dados
            SET NOME = %s, PRECO = %s
            WHERE id = %s
            """, 
            (nome, preco, id)
        )
            self.conn.commit()
            print("\nDados atualizados com sucesso!\n")
        except (Exception, Error) as erro:
            print("Erro ao atualizar dados:", erro)
    def excluir_dados(self, id):
        try:
            self.cur.execute("""
            DELETE FROM tabela_de_dados
            WHERE id = %s
            """,
            (id,)
            )
            self.conn.commit()
            print("\nDados excluídos com sucesso!\n")
        except (Exception, Error) as erro:
            print("Erro ao excluir dados:", erro)

    
