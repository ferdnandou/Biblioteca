import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Conectar ao banco de dados SQLite (não excluir)
conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()

# Criar tabelas se não existirem
cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor_id INTEGER,
    genero TEXT NOT NULL,
    unidades INTEGER NOT NULL,
    FOREIGN KEY (autor_id) REFERENCES autores(id)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS autores (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    status TEXT DEFAULT 'Ativo'
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY,
    usuario_id INTEGER,
    livro_id INTEGER,
    unidades INTEGER,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
)''')

# Função para atualizar visualizações
def atualizar_dados_livros():
    for widget in frame_visualizacao_livros.winfo_children():
        widget.destroy()

    # Atualizar visualização de livros
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    for livro in livros:
        tk.Label(frame_visualizacao_livros, text=f'ID: {livro[0]}, Título: {livro[1]}, Autor ID: {livro[2]}, Gênero: {livro[3]}, Unidades: {livro[4]}').pack(fill='x')

def atualizar_dados_autores():
    for widget in frame_visualizacao_autores.winfo_children():
        widget.destroy()

    # Atualizar visualização de autores
    cursor.execute('SELECT * FROM autores')
    autores = cursor.fetchall()
    for autor in autores:
        tk.Label(frame_visualizacao_autores, text=f'ID: {autor[0]}, Nome: {autor[1]}').pack(fill='x')

def atualizar_dados_usuarios():
    for widget in frame_visualizacao_usuarios.winfo_children():
        widget.destroy()

    # Atualizar visualização de usuários
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        tk.Label(frame_visualizacao_usuarios, text=f'ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Status: {usuario[3]}').pack(fill='x')

def atualizar_dados_emprestimos():
    for widget in frame_visualizacao_emprestimos.winfo_children():
        widget.destroy()

    # Atualizar visualização de empréstimos
    cursor.execute('SELECT * FROM emprestimos')
    emprestimos = cursor.fetchall()
    for emprestimo in emprestimos:
        tk.Label(frame_visualizacao_emprestimos, text=f'ID: {emprestimo[0]}, Usuário ID: {emprestimo[1]}, Livro ID: {emprestimo[2]}, Unidades: {emprestimo[3]}').pack(fill='x')

# Função para adicionar livro
def adicionar_livro(titulo, autor_id, genero, unidades):
    if titulo and autor_id.isdigit() and genero and unidades.isdigit():
        cursor.execute('INSERT INTO livros (titulo, autor_id, genero, unidades) VALUES (?, ?, ?, ?)', (titulo, int(autor_id), genero, int(unidades)))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Livro adicionado com sucesso!')
        atualizar_dados_livros()
    else:
        messagebox.showwarning('Atenção', 'Por favor, preencha todos os campos corretamente.')

# Função para adicionar autor
def adicionar_autor(nome):
    if nome:
        cursor.execute('INSERT INTO autores (nome) VALUES (?)', (nome,))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Autor adicionado com sucesso!')
        atualizar_dados_autores()
    else:
        messagebox.showwarning('Atenção', 'Por favor, preencha o nome do autor.')

# Função para adicionar usuário
def adicionar_usuario(nome, email):
    if nome and email:
        cursor.execute('INSERT INTO usuarios (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Usuário adicionado com sucesso!')
        atualizar_dados_usuarios()
    else:
        messagebox.showwarning('Atenção', 'Por favor, preencha todos os campos corretamente.')

# Função para adicionar empréstimo
def adicionar_emprestimo(usuario_id, livro_id, unidades):
    if usuario_id.isdigit() and livro_id.isdigit() and unidades.isdigit():
        cursor.execute('INSERT INTO emprestimos (usuario_id, livro_id, unidades) VALUES (?, ?, ?)', (int(usuario_id), int(livro_id), int(unidades)))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Empréstimo adicionado com sucesso!')
        atualizar_dados_emprestimos()
    else:
        messagebox.showwarning('Atenção', 'Por favor, preencha todos os campos corretamente.')

# Criar interface gráfica
root = tk.Tk()
root.title("Biblioteca Digital")
root.geometry("800x600")  # Definindo uma largura e altura fixas

# Criar o Notebook para as abas
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Criar aba de Livros
aba_livros = tk.Frame(notebook)
notebook.add(aba_livros, text="Livros e Autores")

# Criar aba de Usuários e Empréstimos
aba_usuarios_emprestimos = tk.Frame(notebook)
notebook.add(aba_usuarios_emprestimos, text="Usuários e Empréstimos")

# ---- Conteúdo da aba Livros ----
# Frames para visualização
frame_visualizacao = tk.Frame(aba_livros)
frame_visualizacao.pack(fill='x', padx=10, pady=10)

# Aumentando a largura das visualizações
frame_visualizacao_livros = tk.LabelFrame(frame_visualizacao, text='Livros', bg='#e7e7e7', padx=10, pady=10)
frame_visualizacao_livros.pack(side='left', fill='both', expand=True, padx=(0, 10), ipady=20)

scroll_livros = tk.Scrollbar(frame_visualizacao_livros)
scroll_livros.pack(side='right', fill='y')

canvas_livros = tk.Canvas(frame_visualizacao_livros, yscrollcommand=scroll_livros.set)
canvas_livros.pack(side='left', fill='both', expand=True)
scroll_livros.config(command=canvas_livros.yview)

frame_visualizacao_autores = tk.LabelFrame(frame_visualizacao, text='Autores', bg='#e7e7e7', padx=10, pady=10)
frame_visualizacao_autores.pack(side='left', fill='both', expand=True, ipady=20)

scroll_autores = tk.Scrollbar(frame_visualizacao_autores)
scroll_autores.pack(side='right', fill='y')

canvas_autores = tk.Canvas(frame_visualizacao_autores, yscrollcommand=scroll_autores.set)
canvas_autores.pack(side='left', fill='both', expand=True)
scroll_autores.config(command=canvas_autores.yview)

# Adição de Livros e Autores
frame_adicionar = tk.Frame(aba_livros)
frame_adicionar.pack(pady=10)

# Adicionar Livro
frame_adicionar_livro = tk.LabelFrame(frame_adicionar, text='Adicionar Livro', bg='#e7e7e7', padx=5, pady=5)
frame_adicionar_livro.pack(side='left', padx=(0, 20))

tk.Label(frame_adicionar_livro, text='Título:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_livro_titulo = tk.Entry(frame_adicionar_livro, width=30)
entry_livro_titulo.grid(row=0, column=1)

tk.Label(frame_adicionar_livro, text='ID do Autor:', bg='#e7e7e7').grid(row=1, column=0, sticky="w")
entry_livro_autor_id = tk.Entry(frame_adicionar_livro, width=30)
entry_livro_autor_id.grid(row=1, column=1)

tk.Label(frame_adicionar_livro, text='Gênero:', bg='#e7e7e7').grid(row=2, column=0, sticky="w")
entry_livro_genero = tk.Entry(frame_adicionar_livro, width=30)
entry_livro_genero.grid(row=2, column=1)

tk.Label(frame_adicionar_livro, text='Unidades:', bg='#e7e7e7').grid(row=3, column=0, sticky="w")
entry_livro_unidades = tk.Entry(frame_adicionar_livro, width=30)
entry_livro_unidades.grid(row=3, column=1)

tk.Button(frame_adicionar_livro, text='Adicionar', command=lambda: adicionar_livro(entry_livro_titulo.get(), entry_livro_autor_id.get(), entry_livro_genero.get(), entry_livro_unidades.get())).grid(row=4, columnspan=2, pady=10)

# Adicionar Autor
frame_adicionar_autor = tk.LabelFrame(frame_adicionar, text='Adicionar Autor', bg='#e7e7e7', padx=5, pady=5)
frame_adicionar_autor.pack(side='left', padx=(0, 20))

tk.Label(frame_adicionar_autor, text='Nome:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_autor_nome = tk.Entry(frame_adicionar_autor, width=30)
entry_autor_nome.grid(row=0, column=1)

tk.Button(frame_adicionar_autor, text='Adicionar', command=lambda: adicionar_autor(entry_autor_nome.get())).grid(row=1, columnspan=2, pady=10)

# ---- Conteúdo da aba Usuários e Empréstimos ----
# Frames para visualização
frame_visualizacao_usuarios_emprestimos = tk.Frame(aba_usuarios_emprestimos, bg='#e7e7e7')
frame_visualizacao_usuarios_emprestimos.pack(pady=10, padx=10)

# Frame para Usuários
frame_visualizacao_usuarios = tk.LabelFrame(frame_visualizacao_usuarios_emprestimos, text='Usuários', bg='#e7e7e7', padx=10, pady=10)
frame_visualizacao_usuarios.pack(side='left', fill='both', expand=True, padx=(0, 10))

scroll_usuarios = tk.Scrollbar(frame_visualizacao_usuarios)
scroll_usuarios.pack(side='right', fill='y')

canvas_usuarios = tk.Canvas(frame_visualizacao_usuarios, yscrollcommand=scroll_usuarios.set, height=300)  # Aumente a altura
canvas_usuarios.pack(side='left', fill='both', expand=True)
scroll_usuarios.config(command=canvas_usuarios.yview)

# Frame para Empréstimos
frame_visualizacao_emprestimos = tk.LabelFrame(frame_visualizacao_usuarios_emprestimos, text='Empréstimos', bg='#e7e7e7', padx=10, pady=10)
frame_visualizacao_emprestimos.pack(side='right', fill='both', expand=True, padx=(10, 0))

scroll_emprestimos = tk.Scrollbar(frame_visualizacao_emprestimos)
scroll_emprestimos.pack(side='right', fill='y')

canvas_emprestimos = tk.Canvas(frame_visualizacao_emprestimos, yscrollcommand=scroll_emprestimos.set, height=300)  # Aumente a altura
canvas_emprestimos.pack(side='left', fill='both', expand=True)
scroll_emprestimos.config(command=canvas_emprestimos.yview)

# Adição de Usuários e Empréstimos
frame_adicionar_usuarios_emprestimos = tk.Frame(aba_usuarios_emprestimos)
frame_adicionar_usuarios_emprestimos.pack(pady=10)

# (O restante do código para adicionar usuários e empréstimos permanece o mesmo)

# Adicionar Usuário
frame_adicionar_usuario = tk.LabelFrame(frame_adicionar_usuarios_emprestimos, text='Adicionar Usuário', bg='#e7e7e7', padx=5, pady=5)
frame_adicionar_usuario.pack(side='left', padx=(0, 20))

tk.Label(frame_adicionar_usuario, text='Nome:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_usuario_nome = tk.Entry(frame_adicionar_usuario, width=30)
entry_usuario_nome.grid(row=0, column=1)

tk.Label(frame_adicionar_usuario, text='Email:', bg='#e7e7e7').grid(row=1, column=0, sticky="w")
entry_usuario_email = tk.Entry(frame_adicionar_usuario, width=30)
entry_usuario_email.grid(row=1, column=1)

tk.Button(frame_adicionar_usuario, text='Adicionar', command=lambda: adicionar_usuario(entry_usuario_nome.get(), entry_usuario_email.get())).grid(row=2, columnspan=2, pady=10)

# Adicionar Empréstimo
frame_adicionar_emprestimo = tk.LabelFrame(frame_adicionar_usuarios_emprestimos, text='Adicionar Empréstimo', bg='#e7e7e7', padx=5, pady=5)
frame_adicionar_emprestimo.pack(side='left', padx=(0, 20))

tk.Label(frame_adicionar_emprestimo, text='ID do Usuário:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_emprestimo_usuario_id = tk.Entry(frame_adicionar_emprestimo, width=30)
entry_emprestimo_usuario_id.grid(row=0, column=1)

tk.Label(frame_adicionar_emprestimo, text='ID do Livro:', bg='#e7e7e7').grid(row=1, column=0, sticky="w")
entry_emprestimo_livro_id = tk.Entry(frame_adicionar_emprestimo, width=30)
entry_emprestimo_livro_id.grid(row=1, column=1)

tk.Label(frame_adicionar_emprestimo, text='Unidades:', bg='#e7e7e7').grid(row=2, column=0, sticky="w")
entry_emprestimo_unidades = tk.Entry(frame_adicionar_emprestimo, width=30)
entry_emprestimo_unidades.grid(row=2, column=1)

tk.Button(frame_adicionar_emprestimo, text='Adicionar', command=lambda: adicionar_emprestimo(entry_emprestimo_usuario_id.get(), entry_emprestimo_livro_id.get(), entry_emprestimo_unidades.get())).grid(row=3, columnspan=2, pady=10)

# Atualizar as visualizações ao iniciar
atualizar_dados_livros()
atualizar_dados_autores()
atualizar_dados_usuarios()
atualizar_dados_emprestimos()

# Rodar a aplicação
root.mainloop()

# Fechar conexão com o banco de dados ao encerrar
conn.close()
