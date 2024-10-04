import sqlite3
import tkinter as tk
from tkinter import messagebox

# Conectar ao banco de dados SQLite (não excluir)
conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()

# Criar tabelas se não existirem
cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    genero TEXT NOT NULL,
    unidades INTEGER NOT NULL
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
def atualizar_dados():
    # Limpar as visualizações
    for widget in frame_visualizacao_livros.winfo_children():
        widget.destroy()
    for widget in frame_visualizacao_usuarios.winfo_children():
        widget.destroy()
    for widget in frame_visualizacao_emprestimos.winfo_children():
        widget.destroy()

    # Atualizar visualização de livros
    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()
    for livro in livros:
        tk.Label(frame_visualizacao_livros, text=f'Título: {livro[1]}, Autor: {livro[2]}, Gênero: {livro[3]}, Unidades: {livro[4]}').pack(fill='x')

    # Atualizar visualização de usuários
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        tk.Label(frame_visualizacao_usuarios, text=f'ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Status: {usuario[3]}').pack(fill='x')

    # Atualizar visualização de empréstimos
    cursor.execute('SELECT * FROM emprestimos')
    emprestimos = cursor.fetchall()
    for emprestimo in emprestimos:
        tk.Label(frame_visualizacao_emprestimos, text=f'Usuário ID: {emprestimo[1]}, Livro ID: {emprestimo[2]}, Unidades: {emprestimo[3]}').pack(fill='x')

# Função para adicionar usuário
def adicionar_usuario(nome, email, status='Ativo'):
    if nome and email:
        cursor.execute('INSERT INTO usuarios (nome, email, status) VALUES (?, ?, ?)', (nome, email, status))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Usuário adicionado com sucesso!')
        atualizar_dados()
    else:
        messagebox.showwarning('Atenção', 'Por favor, preencha todos os campos.')

# Função para remover usuário
def remover_usuario(usuario_id):
    if usuario_id.isdigit():
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Usuário removido com sucesso!')
        atualizar_dados()
    else:
        messagebox.showwarning('Atenção', 'Por favor, insira um ID válido.')

# Função para adicionar livro
def adicionar_livro(titulo, autor, genero, unidades):
    if titulo and autor and genero and unidades.isdigit():
        cursor.execute('INSERT INTO livros (titulo, autor, genero, unidades) VALUES (?, ?, ?, ?)', (titulo, autor, genero, unidades))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Livro adicionado com sucesso!')
        atualizar_dados()
    else:
        messagebox.showwarning('Atenção', 'Por favor, preencha todos os campos corretamente.')

# Função para remover livro
def remover_livro(livro_id):
    if livro_id.isdigit():
        cursor.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Livro removido com sucesso!')
        atualizar_dados()
    else:
        messagebox.showwarning('Atenção', 'Por favor, insira um ID válido.')

# Função para adicionar empréstimo
def adicionar_emprestimo(usuario_id, livro_id, unidades):
    if usuario_id.isdigit() and livro_id.isdigit() and unidades.isdigit():
        cursor.execute('SELECT unidades FROM livros WHERE id = ?', (livro_id,))
        resultado = cursor.fetchone()
        if resultado and resultado[0] >= int(unidades):
            cursor.execute('INSERT INTO emprestimos (usuario_id, livro_id, unidades) VALUES (?, ?, ?)', (usuario_id, livro_id, unidades))
            cursor.execute('UPDATE livros SET unidades = unidades - ? WHERE id = ?', (unidades, livro_id))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Empréstimo adicionado com sucesso!')
            atualizar_dados()
        else:
            messagebox.showwarning('Atenção', 'Unidades insuficientes ou livro não encontrado.')
    else:
        messagebox.showwarning('Atenção', 'Por favor, preencha todos os campos corretamente.')

# Função para devolver livro
def devolver_livro(emprestimo_id):
    if emprestimo_id.isdigit():
        cursor.execute('SELECT livro_id, unidades FROM emprestimos WHERE id = ?', (emprestimo_id,))
        resultado = cursor.fetchone()
        if resultado:
            livro_id, unidades = resultado
            cursor.execute('UPDATE livros SET unidades = unidades + ? WHERE id = ?', (unidades, livro_id))
            cursor.execute('DELETE FROM emprestimos WHERE id = ?', (emprestimo_id,))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Devolução realizada com sucesso!')
            atualizar_dados()
        else:
            messagebox.showwarning('Atenção', 'Empréstimo não encontrado.')
    else:
        messagebox.showwarning('Atenção', 'Por favor, insira um ID de empréstimo válido.')

# Criar interface gráfica
root = tk.Tk()
root.title("Biblioteca Digital")
root.geometry("1366x768")  # Definindo uma largura e altura fixas

# Frames
frame_adicionar = tk.Frame(root)
frame_adicionar.pack(side=tk.LEFT, padx=10, pady=10, fill='y')

frame_visualizacao = tk.Frame(root)
frame_visualizacao.pack(side=tk.RIGHT, padx=10, pady=10, fill='both', expand=True)

# Adicionar Livro
frame_adicionar_livro = tk.LabelFrame(frame_adicionar, text='Adicionar Livro', bg='#e7e7e7', padx=5, pady=5)
frame_adicionar_livro.pack(fill='both', expand=True)

tk.Label(frame_adicionar_livro, text='Título:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_livro_titulo = tk.Entry(frame_adicionar_livro, width=30)
entry_livro_titulo.grid(row=0, column=1)

tk.Label(frame_adicionar_livro, text='Autor:', bg='#e7e7e7').grid(row=1, column=0, sticky="w")
entry_livro_autor = tk.Entry(frame_adicionar_livro, width=30)
entry_livro_autor.grid(row=1, column=1)

tk.Label(frame_adicionar_livro, text='Gênero:', bg='#e7e7e7').grid(row=2, column=0, sticky="w")
entry_livro_genero = tk.Entry(frame_adicionar_livro, width=30)
entry_livro_genero.grid(row=2, column=1)

tk.Label(frame_adicionar_livro, text='Unidades:', bg='#e7e7e7').grid(row=3, column=0, sticky="w")
entry_livro_unidades = tk.Entry(frame_adicionar_livro, width=30)
entry_livro_unidades.grid(row=3, column=1)

tk.Button(frame_adicionar_livro, text='Adicionar Livro', command=lambda: adicionar_livro(entry_livro_titulo.get(), entry_livro_autor.get(), entry_livro_genero.get(), entry_livro_unidades.get()), width=20).grid(row=4, columnspan=2, pady=5)

# Remover Livro
frame_remover_livro = tk.LabelFrame(frame_adicionar, text='Remover Livro', bg='#e7e7e7', padx=5, pady=5)
frame_remover_livro.pack(fill='both', expand=True)

tk.Label(frame_remover_livro, text='ID do Livro:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_remover_livro_id = tk.Entry(frame_remover_livro, width=30)
entry_remover_livro_id.grid(row=0, column=1)

tk.Button(frame_remover_livro, text='Remover Livro', command=lambda: remover_livro(entry_remover_livro_id.get()), width=20).grid(row=1, columnspan=2, pady=5)

# Adicionar Usuário
frame_adicionar_usuario = tk.LabelFrame(frame_adicionar, text='Adicionar Usuário', bg='#e7e7e7', padx=5, pady=5)
frame_adicionar_usuario.pack(fill='both', expand=True)

tk.Label(frame_adicionar_usuario, text='Nome:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_usuario_nome = tk.Entry(frame_adicionar_usuario, width=30)
entry_usuario_nome.grid(row=0, column=1)

tk.Label(frame_adicionar_usuario, text='Email:', bg='#e7e7e7').grid(row=1, column=0, sticky="w")
entry_usuario_email = tk.Entry(frame_adicionar_usuario, width=30)
entry_usuario_email.grid(row=1, column=1)

tk.Button(frame_adicionar_usuario, text='Adicionar Usuário', command=lambda: adicionar_usuario(entry_usuario_nome.get(), entry_usuario_email.get()), width=20).grid(row=2, columnspan=2, pady=5)

# Remover Usuário
frame_remover_usuario = tk.LabelFrame(frame_adicionar, text='Remover Usuário', bg='#e7e7e7', padx=5, pady=5)
frame_remover_usuario.pack(fill='both', expand=True)

tk.Label(frame_remover_usuario, text='ID do Usuário:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_remover_usuario_id = tk.Entry(frame_remover_usuario, width=30)
entry_remover_usuario_id.grid(row=0, column=1)

tk.Button(frame_remover_usuario, text='Remover Usuário', command=lambda: remover_usuario(entry_remover_usuario_id.get()), width=20).grid(row=1, columnspan=2, pady=5)

# Adicionar Empréstimo
frame_adicionar_emprestimo = tk.LabelFrame(frame_adicionar, text='Adicionar Empréstimo', bg='#e7e7e7', padx=5, pady=5)
frame_adicionar_emprestimo.pack(fill='both', expand=True)

tk.Label(frame_adicionar_emprestimo, text='ID do Usuário:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_emprestimo_usuario_id = tk.Entry(frame_adicionar_emprestimo, width=30)
entry_emprestimo_usuario_id.grid(row=0, column=1)

tk.Label(frame_adicionar_emprestimo, text='ID do Livro:', bg='#e7e7e7').grid(row=1, column=0, sticky="w")
entry_emprestimo_livro_id = tk.Entry(frame_adicionar_emprestimo, width=30)
entry_emprestimo_livro_id.grid(row=1, column=1)

tk.Label(frame_adicionar_emprestimo, text='Unidades:', bg='#e7e7e7').grid(row=2, column=0, sticky="w")
entry_emprestimo_unidades = tk.Entry(frame_adicionar_emprestimo, width=30)
entry_emprestimo_unidades.grid(row=2, column=1)

tk.Button(frame_adicionar_emprestimo, text='Adicionar Empréstimo', command=lambda: adicionar_emprestimo(entry_emprestimo_usuario_id.get(), entry_emprestimo_livro_id.get(), entry_emprestimo_unidades.get()), width=20).grid(row=3, columnspan=2, pady=5)

# Devolver Livro
frame_devolver = tk.LabelFrame(frame_adicionar, text='Devolver Livro', bg='#e7e7e7', padx=5, pady=5)
frame_devolver.pack(fill='both', expand=True)

tk.Label(frame_devolver, text='ID do Empréstimo:', bg='#e7e7e7').grid(row=0, column=0, sticky="w")
entry_devolver_id = tk.Entry(frame_devolver, width=30)
entry_devolver_id.grid(row=0, column=1)

# Ajustar a posição do botão e diminuir o tamanho
devolver_button = tk.Button(frame_devolver, text='Devolver', command=lambda: devolver_livro(entry_devolver_id.get()), width=15)  # Diminuindo largura do botão
devolver_button.grid(row=1, columnspan=2, pady=5)

# Frame de visualização
frame_visualizacao_livros = tk.LabelFrame(frame_visualizacao, text='Livros', bg='#e7e7e7', padx=10, pady=10)
frame_visualizacao_livros.pack(fill='both', expand=True)

frame_visualizacao_usuarios = tk.LabelFrame(frame_visualizacao, text='Usuários', bg='#e7e7e7', padx=10, pady=10)
frame_visualizacao_usuarios.pack(fill='both', expand=True)

frame_visualizacao_emprestimos = tk.LabelFrame(frame_visualizacao, text='Empréstimos', bg='#e7e7e7', padx=10, pady=10)
frame_visualizacao_emprestimos.pack(fill='both', expand=True)

# Atualizar visualizações ao iniciar
atualizar_dados()

root.mainloop()

# Fechar a conexão com o banco de dados ao sair
conn.close()
