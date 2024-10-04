# Biblioteca Digital

Este projeto é uma aplicação simples de uma Biblioteca Digital usando Python, SQLite e Tkinter. Ele permite gerenciar livros, usuários e empréstimos através de uma interface gráfica fácil de usar.

## Funcionalidades

- **Gerenciamento de Livros:**
  - Adicionar novos livros com título, autor, gênero e número de unidades disponíveis.
  - Remover livros existentes.
  
- **Gerenciamento de Usuários:**
  - Adicionar novos usuários com nome, e-mail e status (Ativo por padrão).
  - Remover usuários do sistema.
  
- **Empréstimos:**
  - Registrar empréstimos de livros aos usuários.
  - Devolver livros e atualizar automaticamente a quantidade de unidades disponíveis.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para construir a aplicação.
- **SQLite**: Banco de dados relacional leve para armazenar informações de livros, usuários e empréstimos.
- **Tkinter**: Biblioteca padrão do Python para construção da interface gráfica.

## Como Executar o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/ferdnandou/Biblioteca.git
   ```

2. Navegue até a pasta do projeto:
   ```bash
   cd Biblioteca
   ```

3. Execute o script principal:
   ```bash
   python biblioteca.py
   ```

> **Nota:** Certifique-se de ter o Python instalado em sua máquina. A aplicação criará automaticamente o arquivo `biblioteca.db` se ele não existir.

## Estrutura do Banco de Dados

- **livros**: Armazena informações dos livros (id, título, autor, gênero, unidades).
- **usuarios**: Armazena informações dos usuários (id, nome, e-mail, status).
- **emprestimos**: Registra os empréstimos feitos pelos usuários (id, id do usuário, id do livro, unidades).

## Interface

A interface foi desenvolvida com **Tkinter** e possui uma disposição clara para gerenciar os dados da biblioteca. A tela principal contém:

- Seções para adicionar e remover livros.
- Seções para adicionar e remover usuários.
- Seções para registrar e devolver empréstimos.
- Visualizações de todos os livros, usuários e empréstimos cadastrados no banco de dados.

## Melhorias Futuras

- Adicionar a funcionalidade de pesquisa por livro e usuário.
- Implementar uma funcionalidade para editar as informações dos livros e usuários.

## Contribuição

Sinta-se à vontade para contribuir com melhorias e novas funcionalidades. Basta abrir uma pull request ou reportar issues.

---

**Autor:** [Miguel (ferdnandou)](https://github.com/ferdnandou)
