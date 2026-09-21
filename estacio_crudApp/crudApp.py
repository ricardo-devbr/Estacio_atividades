import psycopg2
from psycopg2 import Error

# FUNCAO PARA CONECTAR AO DB
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host = "localhost",
            database = "crud_app",
            user = "ricardo",
            password = "tomzy2219",
            )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao Banco de dados {e}")
        return None

def create_contact():
    nome = input('Digite o nome: ')
    telefone = input('Digite o telefone: ')
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO public. "AGENDA_DE_CONTATOS" (nome, telefone)
            VALUES (%s, %s) RETURNING id;
            """, (nome, telefone))
            contact_id = cursor.fetchone()[0]
            conn.commit()
            print(f"\nContato criado com sucesso!\nID do contato: {contact_id}")
        except Error as e:
                print(f"Erro ao criar contato: {e}")
        finally:
            cursor.close()
            conn.close()

def read_contact():
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT id, nome, telefone FROM public."AGENDA_DE_CONTATOS";
            """)
            contacts = cursor.fetchall()
            for contact in contacts:
                print(f'\nID: {contact[0]}, Nome: {contact[1]}, Telefone: {contact[2]}')
        except Error as e:
            print(f"Erro ao ler contatos: {e}")
        finally:
            cursor.close()
            conn.close()

def update_contact(contact_id, new_name, new_phone):
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            UPDATE public."AGENDA_DE_CONTATOS"
            SET nome = %s, telefone = %s
            WHERE id = %s;
            """, (new_name, new_phone, contact_id))
            conn.commit()
            print(f"Contato atualizado com sucesso.")
        except Error as e:
            print(f"Erro ao atualizar contato: {e}")
        finally:
            cursor.close()
            conn.close()

def delete_contact(contact_id):
    conn = connect_to_db()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("""
            DELETE FROM public."AGENDA_DE_CONTATOS"
            WHERE id = %s;
            """, (contact_id,))
            conn.commit()
            print(f"Contato deletado com sucesso.")
        except Error as e:
            print(f"Erro ao deletar contato: {e}")
        finally:
            cursor.close()
            conn.close()

def main():
    while True:
        print('\nMenu:')
        print('1 - Criar contato')
        print('2 - Exibir contatos')
        print('3 - Atualizar contato')
        print('4 - Excluir contato')
        print('5 - Sair')

        choice = input('Escolha uma opção: ')
        try:
            choice = int(choice)
        except ValueError:
            print('Opção inválida')
            continue

        match choice:
            case 1:
                create_contact()
            case 2:
                read_contact()
            case 3:
                contact_id = input('Digite o ID do contato: ')
                new_name = input('Digite o novo nome: ')
                new_phone = input('Digite o novo telefone: ')
                update_contact(contact_id, new_name, new_phone)
            case 4:
                contact_id = input('Digite o ID do contato: ')
                delete_contact(contact_id)
            case 5:
                print("Saindo do programa...")
                break
            case _:
                print('Opção inválida')

if __name__ == "__main__":
    main()