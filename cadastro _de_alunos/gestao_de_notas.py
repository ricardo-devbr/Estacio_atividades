import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd


# Prototipo de um sistema escolar: permite informar duas notas, calcular a media
# e mostrar a situacao do aluno em uma tabela. Os registros tambem sao lidos e
# gravados em uma planilha Excel chamada planilhaAlunos.xlsx.
class PrincipalRAD:
    def __init__(self, janela):
        # janela principal que contem os campos usados para identificar o
        # aluno, nota 1 e nota 2 + botao que chama o metodo que calcula a situacao do aluno
        self.lblNome = tk.Label(janela, text="Nome do aluno:")  
        self.lblNota1 = tk.Label(janela, text="Nota 1:")
        self.lblNota2 = tk.Label(janela, text="Nota 2:")    
        self.txtNome=tk.Entry(janela, bd=3)
        self.txtNota1=tk.Entry(janela)
        self.txtNota2=tk.Entry(janela)
        self.btnCalcular = tk.Button(janela, text="Calcular", command=self.fCalcularMedia)

        # Define a ordem das informacoes apresentadas em cada linha da tabela
        self.dadosColunas = ("Aluno", "Nota 1", "Nota 2", "Media", "Situacao")

        # Treeview que exibe os resultados em formato de tabela 
        self.treeMedias = ttk.Treeview(
            janela,
            columns=self.dadosColunas,
            selectmode='browse',
            show='headings',
        )
    
        # barra lateral vertical que permite percorrer os registros quando nao couberem na tela.
        self.verscrlbar = ttk.Scrollbar(janela, orient='vertical', command=self.treeMedias.yview)
        self.treeMedias.configure(yscrollcommand=self.verscrlbar.set)        

        # Ajusta texto mostrado no cabecalho de cada coluna.
        self.treeMedias.heading('Aluno', text='Aluno')
        self.treeMedias.heading('Nota 1', text='Nota 1')
        self.treeMedias.heading('Nota 2', text='Nota 2')
        self.treeMedias.heading('Media', text='Media')
        self.treeMedias.heading('Situacao', text='Situacao')

        # Define a largura inicial de cada coluna
        self.treeMedias.column('Aluno', minwidth=0,width=100)
        self.treeMedias.column('Nota 1', minwidth=0,width=100)
        self.treeMedias.column('Nota 2', minwidth=0,width=100)
        self.treeMedias.column('Media', minwidth=0,width=100)            
        self.treeMedias.column('Situacao', minwidth=0,width=100)

        # Posiciona os campos, botao e tabela na janela usando as coordenadas x e y.
        self.lblNome.place(x=100, y=50)
        self.txtNome.place(x=200, y=50)

        self.lblNota1.place(x=100,y=100)
        self.txtNota1.place(x=200, y=100)

        self.lblNota2.place(x=100,y=150)
        self.txtNota2.place(x=200, y=150)

        self.btnCalcular.place(x=100, y=200)

        self.treeMedias.place(x=100, y=300, width=700, height=225)
        self.verscrlbar.place(x=805, y=300, height=225) 

        # iid e o identificador de cada linha da Treeview e precisa ser unico.
        self.iid = 0

        # Tenta carregar tabela com os registros que ja estao na planilha.
        self.carregarDadosIniciais()

    # funcao para carregar tabela com resgsitro na planilha
    def carregarDadosIniciais(self):
        fsave = 'planilhaAlunos.xlsx'
        try:
            dados = pd.read_excel(fsave)
        except FileNotFoundError:
            print(f"Planilha {fsave} ainda nao existe; ela sera criada ao salvar.")
            return
        except Exception as erro:
            messagebox.showerror("Erro ao carregar", f"Nao foi possivel ler a planilha:\n{erro}")
            return
        # compara as colunas da planilha com a esperadas (aluno, not1, nota 2, media, situacao)
        # e insere os valores na Treeview
        colunas_esperadas = set(self.dadosColunas)
        colunas_ausentes = colunas_esperadas.difference(dados.columns)
        if colunas_ausentes:
            faltantes = ", ".join(sorted(colunas_ausentes))
            messagebox.showerror(
                "Planilha invalida",
                f"Estao faltando estas colunas na planilha: {faltantes}",
            )
            return

        # insere uma linha na tabela para cada registro lido do Excel junto com um idenfificador
        for valores in dados.loc[:, self.dadosColunas].itertuples(index=False, name=None):
            self.treeMedias.insert('', 'end', iid=self.iid, values=valores)
            self.iid += 1

    def fSalvarDados(self):
        #  salva os valores da tabela e sobrescreve a planilha excel
        try:
            fsave = 'planilhaAlunos.xlsx'
            dados = []

            # percorre as linhas da Treeview e coleta os valores de cada uma.
            for line in self.treeMedias.get_children():
                lstDados = []
                for value in self.treeMedias.item(line)['values']:
                 lstDados.append(value)

            # ATENCAO: este append esta fora do loop das linhas. Assim, no
            # estado atual, somente lstDados da ultima linha e adicionada.
                dados.append(lstDados)

            # cria uma tabela pandas com os cabecalhos definidos no inicio
            df = pd.DataFrame(data=dados, columns=self.dadosColunas)

            # grava o arquivo no diretorio de execucao e substitui o
            # conteudo anterior, na aba 'Inconsistencias'.
            planilha = pd.ExcelWriter(fsave)
            df.to_excel(planilha, sheet_name='Inconsistencias', index=False)

            planilha.close()
            print('Dados salvos')
        except Exception as erro:
            messagebox.showerror("Erro ao salvar", f"Nao foi possivel salvar os dados:\n{erro}")


    def fVerificarSituacao(self, nota1, nota2):
        # calcula a média e retorna um texto informando se foi aprovado, reprovado ou em recuperacao
        media = (nota1+nota2)/2
        if(media >= 7.0):
            situacao = 'Aprovado'
        elif (media >= 5.0):
            situacao = 'Em recuperacao'
        else:
            situacao = 'Reprovado'
        return media, situacao
    
    # le os campos, calcula o resultado, atualiza a tabela e salva
    def fCalcularMedia(self): 
        try:
            nome = self.txtNome.get().strip()
            if not nome:
                raise ValueError("Informe o nome do aluno.")

            nota1 = float(self.txtNota1.get().replace(',', '.'))
            nota2 = float(self.txtNota2.get().replace(',', '.'))
            if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10):
                raise ValueError("As notas devem estar entre 0 e 10.")
        except ValueError as erro:
            messagebox.showerror("Dados invalidos", str(erro))
            return

        media, situacao = self.fVerificarSituacao(nota1, nota2)

        # Mostra os dados calculados em uma nova linha e salva a tabela.
        self.treeMedias.insert(
            '', 'end', iid=self.iid,
            values=(nome, str(nota1), str(nota2), str(media), situacao),
        )
        self.iid += 1
        self.fSalvarDados()

        # Limpa os campos depois de um cadastro valido.
        self.txtNome.delete(0, 'end')
        self.txtNota1.delete(0, 'end')
        self.txtNota2.delete(0, 'end')

# inicia a janela de interacao
janela=tk.Tk()
principal = PrincipalRAD(janela)
janela.title('Bem vindo ao RAD')
janela.geometry('820x600')
janela.mainloop()