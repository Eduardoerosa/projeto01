import sqlite3  # Biblioteca para trabalhar com banco de dados SQLite
import customtkinter# Biblioteca para criar a interface moderna
 
# Configura o visual do app (modo escuro e tema azul)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
 
# Função para conectar ou criar o banco de dados
def conectar():
    return sqlite3.connect("banco.db")  # Cria arquivo banco.db se não existir
 
# Função que cria a tabela de produtos no banco (caso ainda não exista)
def criar_tabela():
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT NOT NULL,preco REAL NOT NULL)''')
    con.commit()  # Salva as alterações
    con.close()   # Fecha a conexão com o banco
 
# Função que adiciona um novo produto ao banco
def adicionar_produto():
    nome = entrada_nome.get()  # Pega o texto digitado no campo de nome
    try:
        preco = float(entrada_preco.get())  # Converte o texto do campo de preço para número
    except ValueError:
        # Se o valor não for número, exibe mensagem de erro
        resultado.configure(text="Preço inválido.", text_color="red")
        return
 
    # Insere o produto no banco
    con = conectar()
    cur = con.cursor()
    cur.execute('INSERT INTO produtos (nome, preco) VALUES (?, ?)', (nome, preco))
    con.commit()
    con.close()
 
    # Exibe confirmação e limpa os campos
    resultado.configure(text="Produto adicionado com sucesso!", text_color="green")
    entrada_nome.delete(0, customtkinter.END)
    entrada_preco.delete(0, customtkinter.END)
 
# Função que lista os produtos com preço maior que R$100
def listar_produtos():
    con = conectar()
    cur = con.cursor()
    cur.execute('SELECT * FROM produtos WHERE preco > 100')  # Seleciona produtos com preço > 100
    produtos = cur.fetchall()
    con.close()
 
    # Monta um texto com os produtos encontrados
    texto = "Produtos com preço > R$100:\n"
    if produtos:
        for p in produtos:
            texto += f"ID: {p[0]} | Nome: {p[1]} | Preço: R${p[2]:.2f}\n"
    else:
        texto += "Nenhum produto encontrado."
 
    resultado.configure(text=texto, text_color="white")
criar_tabela()
# Criação da janela principal do app
app = customtkinter.CTk()
app.title("Cadastro de Produtos")     # Título da janela
app.geometry("500x400")              # Tamanho da janela
 
# Título na interface
titulo = customtkinter.CTkLabel(app, text="Sistema de Produtos", font=("Arial", 20))
titulo.pack(pady=10)
 
# Campo de entrada para o nome do produto
entrada_nome = customtkinter.CTkEntry(app, placeholder_text="Nome do produto")
entrada_nome.pack(pady=5)
 
# Campo de entrada para o preço do produto
entrada_preco = customtkinter.CTkEntry(app, placeholder_text="Preço do produto")
entrada_preco.pack(pady=5)
 
# Botão que chama a função para adicionar produto
botao_adicionar = customtkinter.CTkButton(app, text="Adicionar Produto", command=adicionar_produto)
botao_adicionar.pack(pady=10)
 
# Botão que chama a função para listar produtos > R$100
botao_listar = customtkinter.CTkButton(app, text="Listar Produtos > R$100", command=listar_produtos)
botao_listar.pack(pady=5)
 
# Área onde o resultado das ações vai aparecer (mensagens, lista, etc)
resultado = customtkinter.CTkLabel(app, text="", wraplength=480, justify="left")
resultado.pack(pady=20)
 
# Inicializa a tabela no banco e abre a janela

app.mainloop()