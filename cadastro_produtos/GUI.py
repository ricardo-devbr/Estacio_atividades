# INTERFACE GRAFICA COM BOTOES E EXECUCAO DE ACOES DO USUARIO
# E DADOS FALSOS GERADOS PARA TESTE
# É POSSIVEL CADASTRAR, ATUALIZAR EXCLUIR PRODUTO,
# ALEM DE LIMPAR O CAMPO DE ENTRADA DE TEXTO
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from produto_DB import AppBD
from faker import Faker

# CRIA A INTERFACE GRAFICA
class principal:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title('Interface de produtos')

        # COMPONENTES DA GUI
        self.id = tk.Label(root, text='Código:')
        self.id.grid(row=0, column=0)
        self.txtid = tk.Entry(root)
        self.txtid.grid(row=0, column=1)

        self.lblnome = tk.Label(root, text='Nome:')
        self.lblnome.grid(row=1, column=0)
        self.txtnome = tk.Entry(root)
        self.txtnome.grid(row=1, column=1)

        self.lblpreco = tk.Label(root, text='Preço:')
        self.lblpreco.grid(row=2, column=0)
        self.txtpreco = tk.Entry(root)
        self.txtpreco.grid(row=2, column=1)

        # BOTOES
        self.btncadastrar = tk.Button(root, text='Cadastrar', command=self.fCadastrar_produto)
        self.btncadastrar.grid(row=3, column=0, columnspan=2)
        
        self.btnatualizar = tk.Button(root, text='Atualizar', command=self.fAtualizar_produto)
        self.btnatualizar.grid(row=4, column=0, columnspan=2)

        self.btnexcluir = tk.Button(root, text='Excluir', command=self.fExcluir_produto)
        self.btnexcluir.grid(row=5, column=0, columnspan=2)

        self.btnlimpar = tk.Button(root, text='Limpar', command=self.fLimpar_tela)
        self.btnlimpar.grid(row=6, column=0, columnspan=2)

        # TREE VIEW
        self.tree = ttk.Treeview(root, columns=('Codigo', 'Nome', 'Preco'), show='headings')
        self.tree.heading('Codigo', text='Código')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Preco', text='Preço')
        self.tree.grid(row=7, column=0, columnspan=2)
        self.tree.bind('<ButtonRelease-1>', self.fApresentar_registros_selecionados)

        self.carregarDadosiniciais()

# FUNCAO QUE CADASTRA PRODUTOS
    def fCadastrar_produto(self):
        nome = self.txtnome.get()
        preco = self.txtpreco.get()
        self.db.inserir_dados(nome, preco)
        self.fLimpar_tela()
        self.carregarDadosiniciais()  # Recarrega a tabela com o código real gerado pelo PostgreSQL
            
# FUNCAO QUE ATUALIZA PRODUTO COM BASE EM UM ID
    def fAtualizar_produto(self):
        id = self.txtid.get().strip()
        if not id.isdigit():
            messagebox.showwarning("Código inválido", "Selecione um produto com código válido antes de atualizar.")
            return

        nome = self.txtnome.get()
        preco = self.txtpreco.get()
        self.db.atualizar_dados(id, nome, preco)
        self.fLimpar_tela()
        self.carregarDadosiniciais()

# FUNCAO QUE EXCLUI PRODUTO COM BASE NO ID OU APENAS SELECIOANDO NA TREEVIEW
    def fExcluir_produto(self):
        id = self.txtid.get().strip()
        if not id.isdigit():
            messagebox.showwarning("Código inválido", "Selecione um produto com código válido antes de excluir.")
            return

        self.db.excluir_dados(id)
        self.fLimpar_tela()
        self.carregarDadosiniciais()

# LIMPA OS CAMPOS DE TEXTO
    def fLimpar_tela(self):
        self.txtid.delete(0, tk.END)
        self.txtnome.delete(0, tk.END)
        self.txtpreco.delete(0, tk.END)

# FUNCAO QUE PERMITE SELECIONAR UM LINHA NA TABELA CLICANDO
# ELA ENVIA OS VALORES DA LINHA SELECIONADA PARA OS CAMPOS DE TEXTO
    def fApresentar_registros_selecionados(self, event):
        selecao = self.tree.selection()
        if not selecao:
            return
        item = selecao[0]
        valores = self.tree.item(item, 'values')
        self.txtid.delete(0, tk.END)
        self.txtid.insert(0, valores[0])
        self.txtnome.delete(0, tk.END)
        self.txtnome.insert(0, valores[1])
        self.txtpreco.delete(0, tk.END)
        self.txtpreco.insert(0, valores[2])

# EXIBE OS DADOS QUE JA ESTAVAM SALVO NO BANCO DE DADOS.
    def carregarDadosiniciais(self):
        for item in self.tree.get_children():
            self.tree.delete(item)  
        registros = self.db.selecionar_dados()
        for registro in registros:
            self.tree.insert('', 'end', values=registro)

# FUNCAO QUE GERA DADOS FALSOS PARA TESTE
def gerar_dados_falsos():
    app_bd = AppBD()
    fake = Faker('pt_BR')

    for _ in range(10):
        nome = fake.word()
        preco = round(fake.random_number(digits=7)/100,2)
        app_bd.inserir_dados(nome, preco)

root = tk.Tk()
app_bd = AppBD()
gerar_dados_falsos()  # Gera dados falsos no banco de dados
app_gui = principal(root, app_bd)
root.mainloop()