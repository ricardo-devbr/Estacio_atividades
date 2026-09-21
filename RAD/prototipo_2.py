import tkinter as tk
from tkinter import ttk
import pandas as pd

janela = tk.Tk()
janela.title("Sistema de gestão Escolar - prototipo")
janela.geometry("1010x400")

tk.Label(janela, text="Nome do aluno:").pack()
entrada_nome = tk.Entry(janela)
entrada_nome.pack()

tk.Label(janela, text="Nota 1:").pack()
entrada_nota1 = tk.Entry(janela)
entrada_nota1.pack()

tk.Label(janela, text="Nota 2:").pack()
entrada_nota2 = tk.Entry(janela)
entrada_nota2.pack()

tabela = ttk.Treeview(janela, columns=("Nome", "Nota 1", "Nota 2", "Média", "Situação"), show="headings")
tabela.heading("Nome", text="Nome")
tabela.heading("Nota 1", text="Nota 1")
tabela.heading("Nota 2", text="Nota 2")
tabela.heading("Média", text="Média")
tabela.heading("Situação", text="Situação")
tabela.pack()

scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tabela.yview)
tabela.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

alunos_iniciais = [
    ("Alice", 8.5, 7.0),
    ("Bob", 6.0, 5.5),
    ("Charlie", 9.0, 8.5),
    ("Diana", 4.0, 6.0)
]

for aluno in alunos_iniciais:
    nome, nota1, nota2 = aluno
    media = (nota1 + nota2) / 2
    situacao = "aprovado" if media >= 7 else "reprovado"
    tabela.insert("", "end", values=(nome, nota1, nota2, media, situacao))

def cadastrar_aluno():
    nome = entrada_nome.get()
    nota1 = float(entrada_nota1.get())
    nota2 = float(entrada_nota2.get())
    media = (nota1 + nota2) / 2
    situacao = "aprovado" if media >= 7 else "reprovado"

    tabela.insert("", "end", values=(nome, nota1, nota2, media, situacao))

tk.Button(janela, text="Cadastrar Aluno", command=cadastrar_aluno).pack(pady=10)
janela.mainloop()