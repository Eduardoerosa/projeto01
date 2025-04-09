'''import customtkinter
import sqlite3



expressao = ""

customtkinter.set_appearance_mode("dark")

janela = customtkinter.CTk()
janela.title("Calculadora")
janela.geometry("455x300")
janela.title("calculadora")


def banco_dados():
    conexao = sqlite3.connect("historico da calculadora")
    terminal_sql = conexao.cursor
    terminal_sql.execute("CREATE TABLE IF NOT EXISTS itens(id INTERGER PRIMARY KEY AUTOINCREMENT, expressao TEXT, resultado TEXT)")
    conexao.commit()
    conexao.close()



    
    
def botao_click(valor):
    global expressao
    expressao += str(valor)
    label_titulo.configure(text=expressao)

def calcular():
    global expressao
    try:
        resultado = str(eval(expressao))
        label_titulo.configure(text=resultado)
        terminal_sql = conexao.cursor
        terminal_sql.execute("INSERT INTO calculadora(expressao,resultado) VALUES (?,?)",(expressao,resultado))
        conexao.commit()
        conexao.close()
        expressao = resultado
    except:
        label_titulo.configure(text="Erro")
        expressao = ""

def limpar():
    global expressao
    expressao = ""
    label_titulo.configure(text = "")


label_titulo = customtkinter.CTkLabel(janela,text="Calculadora Amadora",text_color="orange")
label_titulo.grid(pady=5,row=1,column=1)

botao1 = customtkinter.CTkButton(janela,text="1",width=100, fg_color="#3e4144", command=lambda: botao_click(1))
botao1.grid(pady=10, row=2,column=0, padx=5)

botao2 = customtkinter.CTkButton(janela,text="2",width=100, fg_color="#3e4144", command=lambda: botao_click(2))
botao2.grid(pady=10,row=2,column=1)

botao3 = customtkinter.CTkButton(janela,text="3",width=100, fg_color="#3e4144", command=lambda: botao_click(3))
botao3.grid(pady=10,row=2,column=2)


botao4 = customtkinter.CTkButton(janela,text="4",width=100, fg_color="#3e4144", command=lambda: botao_click(4))
botao4.grid(pady=10,row=3,column=0)


botao5 = customtkinter.CTkButton(janela,text="5",width=100, fg_color="#3e4144", command=lambda: botao_click(5))
botao5.grid(pady=10,row=3,column=1)


botao6 = customtkinter.CTkButton(janela,text="6",width=100, fg_color="#3e4144", command=lambda: botao_click(6))
botao6.grid(pady=10,row=3,column=2)


botao7 = customtkinter.CTkButton(janela,text="7",width=100, fg_color="#3e4144", command=lambda: botao_click(7))
botao7.grid(pady=10,row=4,column=0)


botao8 = customtkinter.CTkButton(janela,text="8",width=100, fg_color="#3e4144", command=lambda: botao_click(8))
botao8.grid(pady=10,row=4,column=1)


botao9 = customtkinter.CTkButton(janela,text="9",width=100, fg_color="#3e4144", command=lambda: botao_click(9))
botao9.grid(pady=10,row=4,column=2)

botao0 = customtkinter.CTkButton(janela,text="0",width=100, fg_color="#3e4144", command=lambda: botao_click(0))
botao0.grid(pady=10,row=5,column=0)

botao_mais = customtkinter.CTkButton(janela,text="+",width=100, command=lambda: botao_click("+"))
botao_mais.grid(pady=10,row=5,column=1)

botao_menos = customtkinter.CTkButton(janela,text="-",width=100, command=lambda: botao_click("-"))
botao_menos.grid(pady=10,row=5,column=2)

botao_divisao = customtkinter.CTkButton(janela,text="/",width=100, command=lambda: botao_click("/"))
botao_divisao.grid(pady=10,row=5,column=3)

botao_muliplicacao = customtkinter.CTkButton(janela,text="*",width=100, command=lambda: botao_click("*"))
botao_muliplicacao.grid(pady=10,row=4,column=3)

botao_apagar = customtkinter.CTkButton(janela,text="C",width=100, fg_color="red",command=lambda:limpar())
botao_apagar.grid(pady=10,row=3,column=3,padx=20)

botao_igual = customtkinter.CTkButton(janela,text="=",width=100, fg_color="green",command=lambda:calcular())
botao_igual.grid(pady=10,row=2,column=3,padx=5)



janela.mainloop()'''

import customtkinter
import sqlite3

expressao = ""

customtkinter.set_appearance_mode("dark")

janela = customtkinter.CTk()
janela.title("Calculadora")
janela.geometry("455x300")

# Criar a conexão como variável global
conexao = None

def banco_dados():
    global conexao
    conexao = sqlite3.connect("historico_calculadora.db")  # Arquivo de banco de dados
    terminal_sql = conexao.cursor()
    terminal_sql.execute("""CREATE TABLE IF NOT EXISTS calculadora(
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         expressao TEXT, 
                         resultado TEXT)""")
    conexao.commit()

# Chama a função para criar o banco de dados ao iniciar
banco_dados()

def botao_click(valor):
    global expressao
    expressao += str(valor)
    label_titulo.configure(text=expressao)

def calcular():
    global expressao, conexao
    try:
        resultado = str(eval(expressao))
        label_titulo.configure(text=resultado)
        
        terminal_sql = conexao.cursor()
        terminal_sql.execute("INSERT INTO calculadora(expressao, resultado) VALUES (?, ?)", 
                            (expressao, resultado))
        conexao.commit()
        expressao = resultado
    except Exception as e:
        print(f"Erro: {e}")  # Para debug
        label_titulo.configure(text="Erro")
        expressao = ""

def limpar():
    global expressao
    expressao = ""
    label_titulo.configure(text="")

# Interface gráfica
label_titulo = customtkinter.CTkLabel(janela, text="Calculadora Amadora", text_color="orange")
label_titulo.grid(pady=5, row=1, column=1, columnspan=3)

# Linha 2
botao7 = customtkinter.CTkButton(janela, text="7", width=100, fg_color="#3e4144", command=lambda: botao_click(7))
botao7.grid(pady=10, row=2, column=0, padx=5)

botao8 = customtkinter.CTkButton(janela, text="8", width=100, fg_color="#3e4144", command=lambda: botao_click(8))
botao8.grid(pady=10, row=2, column=1)

botao9 = customtkinter.CTkButton(janela, text="9", width=100, fg_color="#3e4144", command=lambda: botao_click(9))
botao9.grid(pady=10, row=2, column=2)

botao_divisao = customtkinter.CTkButton(janela, text="/", width=100, command=lambda: botao_click("/"))
botao_divisao.grid(pady=10, row=2, column=3)

# Linha 3
botao4 = customtkinter.CTkButton(janela, text="4", width=100, fg_color="#3e4144", command=lambda: botao_click(4))
botao4.grid(pady=10, row=3, column=0)

botao5 = customtkinter.CTkButton(janela, text="5", width=100, fg_color="#3e4144", command=lambda: botao_click(5))
botao5.grid(pady=10, row=3, column=1)

botao6 = customtkinter.CTkButton(janela, text="6", width=100, fg_color="#3e4144", command=lambda: botao_click(6))
botao6.grid(pady=10, row=3, column=2)

botao_multiplicacao = customtkinter.CTkButton(janela, text="*", width=100, command=lambda: botao_click("*"))
botao_multiplicacao.grid(pady=10, row=3, column=3)

# Linha 4
botao1 = customtkinter.CTkButton(janela, text="1", width=100, fg_color="#3e4144", command=lambda: botao_click(1))
botao1.grid(pady=10, row=4, column=0)

botao2 = customtkinter.CTkButton(janela, text="2", width=100, fg_color="#3e4144", command=lambda: botao_click(2))
botao2.grid(pady=10, row=4, column=1)

botao3 = customtkinter.CTkButton(janela, text="3", width=100, fg_color="#3e4144", command=lambda: botao_click(3))
botao3.grid(pady=10, row=4, column=2)

botao_menos = customtkinter.CTkButton(janela, text="-", width=100, command=lambda: botao_click("-"))
botao_menos.grid(pady=10, row=4, column=3)

# Linha 5
botao0 = customtkinter.CTkButton(janela, text="0", width=100, fg_color="#3e4144", command=lambda: botao_click(0))
botao0.grid(pady=10, row=5, column=0)

botao_ponto = customtkinter.CTkButton(janela, text=".", width=100, command=lambda: botao_click("."))
botao_ponto.grid(pady=10, row=5, column=1)

botao_igual = customtkinter.CTkButton(janela, text="=", width=100, fg_color="green", command=calcular)
botao_igual.grid(pady=10, row=5, column=2)

botao_mais = customtkinter.CTkButton(janela, text="+", width=100, command=lambda: botao_click("+"))
botao_mais.grid(pady=10, row=5, column=3)

# Linha 6
botao_apagar = customtkinter.CTkButton(janela, text="C", width=430, fg_color="red", command=limpar)
botao_apagar.grid(pady=10, row=6, column=0, columnspan=4)

# Função para fechar a conexão ao sair
def on_closing():
    global conexao
    if conexao:
        conexao.close()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", on_closing)
janela.mainloop()