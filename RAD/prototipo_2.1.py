import tkinter as tk
from tkinter import ttk
import pandas as pd

class PrincipalRAD:
    def __init__(self, janela):
        # componentes
        self.lblNome = tk.Label(janela, text="Nome do aluno:")  
        self.lblNota1 = tk.Label(janela, text="Nota 1:")
        self.lblNota2 = tk.Label(janela, text="Nota 2:")    
        self.lblmedia = tk.Label(janela, text="Media:") 
        self.txtNome=tk.Entry(janela, bd=3)
        self.txtNota1=tk.Entry(janela)
        self.txtNota2=tk.Entry(janela)
        self.btnCalcular = tk.Button(janela, text="Calcular", command=self.fCalcularMedia)
        # componentes da tabela
        self.dadosColunas = ("Aluno", "Nota 1", "Nota 2", "Media", "Situacao")

        self.treeMedias = ttk.Treeview(janela, columns=self.dadosColunas, selectmode='browse')

        self.verscrlbar = ttk.Scrollbar(janela, orient='vertical', command=self.treeMedias.yview)

        self.verscrlbar.pack(side = 'right', fill='x')

        self.treeMedias.configure(yscrollcommand=self.verscrlbar.set)        

        self.treeMedias.heading('Aluno', text='Aluno')
        self.treeMedias.heading('Nota 1', text='Nota 1')
        self.treeMedias.heading('Nota 2', text='Nota 2')
        self.treeMedias.heading('Media', text='Media')
        self.treeMedias.heading('Situacao', text='Situacao')

        self.treeMedias.column('Aluno', minwidth=0,width=100)
        self.treeMedias.column('Nota 1', minwidth=0,width=100)
        self.treeMedias.column('Nota 2', minwidth=0,width=100)
        self.treeMedias.column('Media', minwidth=0,width=100)            
        self.treeMedias.column('Situacao', minwidth=0,width=100)

        self.treeMedias.pack(padx=10, pady=10)

        # posicao dos componentes da janela
        self.lblNome.place(x=100, y=50)
        self.txtNome.place(x=200, y=50)

        self.lblNota1.place(x=100,y=100)
        self.txtNota1.place(x=200, y=100)

        self.lblNota2.place(x=100,y=150)
        self.txtNota2.place(x=200, y=150)

        self.btnCalcular.place(x=100, y=200)

        self.treeMedias.place(x=100, y=300) 
        self.verscrlbar.place(x=805, y=300, height=225) 

        self.id = 0
        self.iid = 0

        self.carregarDadosIniciais()

    def carregarDadosIniciais(self):
        try:
            fsave = 'planilhaAlunos.xlsx'
            dados = pd.read_excel(fsave)
            print('======== dados disponiveis =========')
            print(dados)

            u=dados.count()
            print('u:' +str(u))
            nn=len(dados['Aluno'])
            for i in range(nn):
                nome = dados['Aluno'][i]
                nota1 = str(dados['Nota1'][i])
                nota2 = str(dados['Nota2'][i])
                media = str(dados['Media'][i])
                situacao=dados['Situacao'][i]

                self.treeMedias.insert('', 'end',iid=self.iid, values=(nome, nota1, nota2, media, situacao))
                self.iid = self.iid + 1
                self.id = self.id + 1
        except:
            print('Ainda nao existem dados para carregar')

    def fSalvarDados(self):
        try:
            fsave = 'planilhaAlunos.xlsx'
            dados = []

            for line in self.treeMedias.get_children():
                lstDados = []
                for value in self.treeMedias.item(line)['values']:
                 lstDados.append(value)

            dados.append(lstDados)

            df = pd.DataFrame(data=dados, columns=self.dadosColunas)

            planilha = pd.ExcelWriter(fsave)
            df.to_excel(planilha, sheet_name='Inconsistencias', index=False)

            planilha.close()
            print('Dados salvos')
        except:
            print('nao foi possivel salvar os dados')


    def fVerificarSituacao(self, nota1, nota2):
        media = (nota1+nota2)/2
        if(media >= 7.0):
            situacao = 'Aprovado'
        elif (media >= 5.0):
            situacao = 'Em recuperacao'
        else:
            situacao = 'Reprovado'
        return media, situacao

    def fCalcularMedia(self):
        try:
            nome = self.txtNome.get()
            nota1 = float(self.txtNota1.get())
            nota2 = float(self.txtNota2.get())
            media, situacao = self.fVerificarSituacao(nota1, nota2)

            self.treeMedias.insert('','end', iid=self.iid, values=(nome,str(nota1), str(nota2),str(media),situacao))

            self.iid = self.iid+1
            self.id = self.id + 1

            self.fSalvarDados()

        except ValueError:
            print('Entre com valores válidos')
        finally:
            self.txtNome.delete(0, 'end')
            self.txtNota1.delete(0, 'end')
            self.txtNota2.delete(0, 'end')

janela=tk.Tk()
principal = PrincipalRAD(janela)
janela.title('Bem vindo ao RAD')
janela.geometry('820x600')
janela.mainloop()