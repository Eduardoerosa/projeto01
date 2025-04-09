import customtkinter  # Importa a biblioteca de interface customizável baseada no tkinter
import sqlite3  # Para usar banco de dados SQLite
from tkinter import messagebox  # Para mostrar mensagens tipo alerta ou confirmação

expressao = ""  # Variável global que vai armazenar os números e operadores digitados

customtkinter.set_appearance_mode("dark")  # Define o tema da calculadora como escuro

janela = customtkinter.CTk()  # Cria a janela principal
janela.title("Calculadora")  # Define o título da janela
janela.geometry("455x350")  # Define o tamanho da janela (aumentei um pouco a altura)

# Variável global pra manter a conexão com o banco
conexao = None

# Função que cria ou conecta ao banco de dados e define a tabela
def banco_dados():
    global conexao
    conexao = sqlite3.connect("historico_calculadora.db")  # Cria/conecta ao banco
    terminal_sql = conexao.cursor()
    terminal_sql.execute("""CREATE TABLE IF NOT EXISTS calculadora(
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         expressao TEXT, 
                         resultado TEXT,
                         data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")  # Cria a tabela se não existir
    conexao.commit()  # Salva alterações

# Chamo logo no começo pra garantir que o banco tá pronto
banco_dados()

# Função chamada quando clico nos botões de número ou operador
def botao_click(valor):
    global expressao
    expressao += str(valor)  # Vai adicionando os valores clicados
    label_titulo.configure(text=expressao)  # Atualiza o texto na tela

# Função que calcula o resultado
def calcular():
    global expressao, conexao
    try:
        resultado = str(eval(expressao))  # Usa eval pra calcular a expressão
        label_titulo.configure(text=resultado)  # Mostra o resultado

        # Salva no banco
        terminal_sql = conexao.cursor()
        terminal_sql.execute("INSERT INTO calculadora(expressao, resultado) VALUES (?, ?)", 
                            (expressao, resultado))
        conexao.commit()
        expressao = resultado  # Coloco o resultado na expressao pra poder continuar calculando
    except Exception as e:
        print(f"Erro: {e}")  # Mostra erro no terminal
        label_titulo.configure(text="Erro")  # Mostra "Erro" na tela
        expressao = ""  # Reseta a expressão

# Função que limpa tudo
def limpar():
    global expressao
    expressao = ""  # Zera a expressão
    label_titulo.configure(text="")  # Limpa a tela

# Função que mostra o histórico numa nova janela
def mostrar_historico():
    try:
        # Nova janela só pro histórico
        janela_historico = customtkinter.CTkToplevel(janela)
        janela_historico.title("Histórico de Cálculos")
        janela_historico.geometry("600x400")

        # Frame com scroll
        frame = customtkinter.CTkFrame(janela_historico)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Caixa de texto pra exibir o histórico
        textbox = customtkinter.CTkTextbox(frame, wrap="none")
        textbox.pack(fill="both", expand=True)

        # Scroll vertical e horizontal
        scroll_y = customtkinter.CTkScrollbar(frame, orientation="vertical", command=textbox.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x = customtkinter.CTkScrollbar(frame, orientation="horizontal", command=textbox.xview)
        scroll_x.pack(side="bottom", fill="x")

        textbox.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # Busca os dados do banco
        cursor = conexao.cursor()
        cursor.execute("SELECT id, expressao, resultado, data_hora FROM calculadora ORDER BY data_hora DESC")
        registros = cursor.fetchall()

        if not registros:
            textbox.insert("end", "Nenhum registro encontrado no histórico.\n")  # Se não tiver nada
        else:
            textbox.insert("end", "ID  | Data/Hora            | Expressão              | Resultado\n")
            textbox.insert("end", "-"*80 + "\n")

            for registro in registros:
                id_reg, expressao, resultado, data_hora = registro
                textbox.insert("end", f"{id_reg:3} | {data_hora:19} | {expressao:22} | {resultado}\n")  # Linha por linha

        textbox.configure(state="disabled")  # Bloqueia edição da caixa de texto

        # Função pra limpar o histórico
        def limpar_historico():
            if messagebox.askyesno("Confirmar", "Deseja realmente apagar todo o histórico?"):
                cursor.execute("DELETE FROM calculadora")
                conexao.commit()
                textbox.configure(state="normal")
                textbox.delete("1.0", "end")
                textbox.insert("end", "Histórico limpo com sucesso.\n")
                textbox.configure(state="disabled")

        # Botão de limpar histórico
        btn_limpar = customtkinter.CTkButton(
            janela_historico, 
            text="Limpar Histórico", 
            fg_color="red", 
            command=limpar_historico
        )
        btn_limpar.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao acessar o histórico:\n{str(e)}")  # Mostra erro

# Label principal no topo
label_titulo = customtkinter.CTkLabel(janela, text="Calculadora Amadora", text_color="orange")
label_titulo.grid(pady=5, row=0, column=0, columnspan=4)

# Criação dos botões - linha por linha
# Linha 1
botao7 = customtkinter.CTkButton(janela, text="7", width=100, fg_color="#3e4144", command=lambda: botao_click(7))
botao7.grid(pady=5, row=1, column=0, padx=5)

botao8 = customtkinter.CTkButton(janela, text="8", width=100, fg_color="#3e4144", command=lambda: botao_click(8))
botao8.grid(pady=5, row=1, column=1)

botao9 = customtkinter.CTkButton(janela, text="9", width=100, fg_color="#3e4144", command=lambda: botao_click(9))
botao9.grid(pady=5, row=1, column=2)

botao_divisao = customtkinter.CTkButton(janela, text="/", width=100, command=lambda: botao_click("/"))
botao_divisao.grid(pady=5, row=1, column=3)

# Linha 2
botao4 = customtkinter.CTkButton(janela, text="4", width=100, fg_color="#3e4144", command=lambda: botao_click(4))
botao4.grid(pady=5, row=2, column=0)

botao5 = customtkinter.CTkButton(janela, text="5", width=100, fg_color="#3e4144", command=lambda: botao_click(5))
botao5.grid(pady=5, row=2, column=1)

botao6 = customtkinter.CTkButton(janela, text="6", width=100, fg_color="#3e4144", command=lambda: botao_click(6))
botao6.grid(pady=5, row=2, column=2)

botao_multiplicacao = customtkinter.CTkButton(janela, text="*", width=100, command=lambda: botao_click("*"))
botao_multiplicacao.grid(pady=5, row=2, column=3)

# Linha 3
botao1 = customtkinter.CTkButton(janela, text="1", width=100, fg_color="#3e4144", command=lambda: botao_click(1))
botao1.grid(pady=5, row=3, column=0)

botao2 = customtkinter.CTkButton(janela, text="2", width=100, fg_color="#3e4144", command=lambda: botao_click(2))
botao2.grid(pady=5, row=3, column=1)

botao3 = customtkinter.CTkButton(janela, text="3", width=100, fg_color="#3e4144", command=lambda: botao_click(3))
botao3.grid(pady=5, row=3, column=2)

botao_menos = customtkinter.CTkButton(janela, text="-", width=100, command=lambda: botao_click("-"))
botao_menos.grid(pady=5, row=3, column=3)

# Linha 4
botao0 = customtkinter.CTkButton(janela, text="0", width=100, fg_color="#3e4144", command=lambda: botao_click(0))
botao0.grid(pady=5, row=4, column=0)

botao_ponto = customtkinter.CTkButton(janela, text=".", width=100, command=lambda: botao_click("."))
botao_ponto.grid(pady=5, row=4, column=1)

botao_igual = customtkinter.CTkButton(janela, text="=", width=100, fg_color="green", command=calcular)
botao_igual.grid(pady=5, row=4, column=2)

botao_mais = customtkinter.CTkButton(janela, text="+", width=100, command=lambda: botao_click("+"))
botao_mais.grid(pady=5, row=4, column=3)

# Linha 5 - Botões maiores
botao_apagar = customtkinter.CTkButton(janela, text="C", width=210, fg_color="red", command=limpar)
botao_apagar.grid(pady=10, row=5, column=0, columnspan=2, padx=5)

botao_historico = customtkinter.CTkButton(janela, text="Histórico", width=210, fg_color="#1f538d", command=mostrar_historico)
botao_historico.grid(pady=10, row=5, column=2, columnspan=2)

# Quando clicar no X pra fechar a janela, fecha também a conexão com o banco
def on_closing():
    global conexao
    if conexao:
        conexao.close()  # Fecha o banco
    janela.destroy()  # Fecha a janela

janela.protocol("WM_DELETE_WINDOW", on_closing)  # Ativa o fechamento personalizado
janela.mainloop()  # Roda o app
