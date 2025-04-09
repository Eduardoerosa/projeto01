import customtkinter
import sqlite3
from tkinter import messagebox

expressao = ""

customtkinter.set_appearance_mode("dark")

janela = customtkinter.CTk()
janela.title("Calculadora")
janela.geometry("455x350")  # Aumentei a altura para acomodar o botão de histórico

# Criar a conexão como variável global
conexao = None

def banco_dados():
    global conexao
    conexao = sqlite3.connect("historico_calculadora.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("""CREATE TABLE IF NOT EXISTS calculadora(
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         expressao TEXT, 
                         resultado TEXT,
                         data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")  # Adicionei campo de data/hora
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
        print(f"Erro: {e}")
        label_titulo.configure(text="Erro")
        expressao = ""

def limpar():
    global expressao
    expressao = ""
    label_titulo.configure(text="")

def mostrar_historico():
    try:
        # Criar nova janela para o histórico
        janela_historico = customtkinter.CTkToplevel(janela)
        janela_historico.title("Histórico de Cálculos")
        janela_historico.geometry("600x400")
        
        # Criar um frame com scrollbar
        frame = customtkinter.CTkFrame(janela_historico)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Textbox para mostrar o histórico
        textbox = customtkinter.CTkTextbox(frame, wrap="none")
        textbox.pack(fill="both", expand=True)
        
        # Adicionar scrollbars
        scroll_y = customtkinter.CTkScrollbar(frame, orientation="vertical", command=textbox.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x = customtkinter.CTkScrollbar(frame, orientation="horizontal", command=textbox.xview)
        scroll_x.pack(side="bottom", fill="x")
        
        textbox.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Buscar dados no banco de dados
        cursor = conexao.cursor()
        cursor.execute("SELECT id, expressao, resultado, data_hora FROM calculadora ORDER BY data_hora DESC")
        registros = cursor.fetchall()
        
        if not registros:
            textbox.insert("end", "Nenhum registro encontrado no histórico.\n")
        else:
            textbox.insert("end", "ID  | Data/Hora            | Expressão              | Resultado\n")
            textbox.insert("end", "-"*80 + "\n")
            
            for registro in registros:
                id_reg, expressao, resultado, data_hora = registro
                textbox.insert("end", f"{id_reg:3} | {data_hora:19} | {expressao:22} | {resultado}\n")
        
        textbox.configure(state="disabled")  # Tornar o texto somente leitura
        
        # Botão para limpar histórico
        def limpar_historico():
            if messagebox.askyesno("Confirmar", "Deseja realmente apagar todo o histórico?"):
                cursor.execute("DELETE FROM calculadora")
                conexao.commit()
                textbox.configure(state="normal")
                textbox.delete("1.0", "end")
                textbox.insert("end", "Histórico limpo com sucesso.\n")
                textbox.configure(state="disabled")
        
        btn_limpar = customtkinter.CTkButton(
            janela_historico, 
            text="Limpar Histórico", 
            fg_color="red", 
            command=limpar_historico
        )
        btn_limpar.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao acessar o histórico:\n{str(e)}")

# Interface gráfica principal
label_titulo = customtkinter.CTkLabel(janela, text="Calculadora Amadora", text_color="orange")
label_titulo.grid(pady=5, row=0, column=0, columnspan=4)

# Linha 1 - Botões 7-9 e divisão
botao7 = customtkinter.CTkButton(janela, text="7", width=100, fg_color="#3e4144", command=lambda: botao_click(7))
botao7.grid(pady=5, row=1, column=0, padx=5)

botao8 = customtkinter.CTkButton(janela, text="8", width=100, fg_color="#3e4144", command=lambda: botao_click(8))
botao8.grid(pady=5, row=1, column=1)

botao9 = customtkinter.CTkButton(janela, text="9", width=100, fg_color="#3e4144", command=lambda: botao_click(9))
botao9.grid(pady=5, row=1, column=2)

botao_divisao = customtkinter.CTkButton(janela, text="/", width=100, command=lambda: botao_click("/"))
botao_divisao.grid(pady=5, row=1, column=3)

# Linha 2 - Botões 4-6 e multiplicação
botao4 = customtkinter.CTkButton(janela, text="4", width=100, fg_color="#3e4144", command=lambda: botao_click(4))
botao4.grid(pady=5, row=2, column=0)

botao5 = customtkinter.CTkButton(janela, text="5", width=100, fg_color="#3e4144", command=lambda: botao_click(5))
botao5.grid(pady=5, row=2, column=1)

botao6 = customtkinter.CTkButton(janela, text="6", width=100, fg_color="#3e4144", command=lambda: botao_click(6))
botao6.grid(pady=5, row=2, column=2)

botao_multiplicacao = customtkinter.CTkButton(janela, text="*", width=100, command=lambda: botao_click("*"))
botao_multiplicacao.grid(pady=5, row=2, column=3)

# Linha 3 - Botões 1-3 e subtração
botao1 = customtkinter.CTkButton(janela, text="1", width=100, fg_color="#3e4144", command=lambda: botao_click(1))
botao1.grid(pady=5, row=3, column=0)

botao2 = customtkinter.CTkButton(janela, text="2", width=100, fg_color="#3e4144", command=lambda: botao_click(2))
botao2.grid(pady=5, row=3, column=1)

botao3 = customtkinter.CTkButton(janela, text="3", width=100, fg_color="#3e4144", command=lambda: botao_click(3))
botao3.grid(pady=5, row=3, column=2)

botao_menos = customtkinter.CTkButton(janela, text="-", width=100, command=lambda: botao_click("-"))
botao_menos.grid(pady=5, row=3, column=3)

# Linha 4 - Botão 0, ponto, igual e adição
botao0 = customtkinter.CTkButton(janela, text="0", width=100, fg_color="#3e4144", command=lambda: botao_click(0))
botao0.grid(pady=5, row=4, column=0)

botao_ponto = customtkinter.CTkButton(janela, text=".", width=100, command=lambda: botao_click("."))
botao_ponto.grid(pady=5, row=4, column=1)

botao_igual = customtkinter.CTkButton(janela, text="=", width=100, fg_color="green", command=calcular)
botao_igual.grid(pady=5, row=4, column=2)

botao_mais = customtkinter.CTkButton(janela, text="+", width=100, command=lambda: botao_click("+"))
botao_mais.grid(pady=5, row=4, column=3)

# Linha 5 - Botão limpar e histórico
botao_apagar = customtkinter.CTkButton(janela, text="C", width=210, fg_color="red", command=limpar)
botao_apagar.grid(pady=10, row=5, column=0, columnspan=2, padx=5)

botao_historico = customtkinter.CTkButton(janela, text="Histórico", width=210, fg_color="#1f538d", command=mostrar_historico)
botao_historico.grid(pady=10, row=5, column=2, columnspan=2)

# Função para fechar a conexão ao sair
def on_closing():
    global conexao
    if conexao:
        conexao.close()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", on_closing)
janela.mainloop()