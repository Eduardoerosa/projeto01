import customtkinter
import tkinter as tk
from tkinter import ttk
import sqlite3


item_vet = 0
checkbox_selecionado = None




# criar banco de dados
def criar_banco():
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("CREATE TABLE IF NOT EXISTS itens (nome text,preco decimal,descricao text,quantidade decimal)")
    conexao.commit()
    conexao.close()

# limpar tela do cadastro
def limpar_campos_cadastro():
    placeholder_digitar_nome_para_framecadastro.delete(0,tk.END)
    ctk_entry_preco_framecadastro.delete(0,tk.END)
    textbox_descricao_framecadastro.delete('1.0',tk.END)


# salvar dados do cadastro
def salvar_dados():
    nome_estoque = placeholder_digitar_nome_para_framecadastro.get()
    preco_estoque = ctk_entry_preco_framecadastro.get()
    descricao_estoque = textbox_descricao_framecadastro.get("1.0","end")
    quantidade = 0
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"INSERT INTO itens VALUES ('{nome_estoque}', '{preco_estoque}', '{descricao_estoque}','{quantidade}')")
    conexao.commit()
    conexao.close()
    limpar_campos_cadastro()

# ler dados
def ler_dados():
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("SELECT * FROM itens")
    recebe_dados = terminal_sql.fetchall()


    for row in tabela_table_wiew_estoque.get_children(): #usado para impedir repetir novos dados no relatório
        tabela_table_wiew_estoque.delete(row)





    for j in recebe_dados:
        nome = str(j[0])
        preco = str(j[1])
        descricao = str(j[2])
        quantidade = str(j[3])
        tabela_table_wiew_estoque.insert('', tk.END, values=(nome,quantidade, preco, descricao))




def ler_dados_mostrar(arg_scrollabelframe):
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("SELECT nome FROM itens")
    recebe_dados = terminal_sql.fetchall()


    for w in arg_scrollabelframe.winfo_children():
        w.destroy()
    
    status = customtkinter.StringVar()
    for i in recebe_dados:
        checkbox = customtkinter.CTkCheckBox(arg_scrollabelframe, text=i, onvalue=i, offvalue="", variable=status, command=lambda:ler_dados_produto(status.get(), arg_scrollabelframe) if status.get() else desmarcar_check_box(arg_scrollabelframe))
        checkbox.pack(pady=5,anchor="w")



def ler_dados_produto(arg_checkbox, arg_scrollabelframe):
    nome = arg_checkbox.strip("(),'")
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"SELECT * FROM itens WHERE nome = '{nome}'")
    recebe_dados_produto = terminal_sql.fetchall()
    if arg_scrollabelframe == scrollabel_lista_frameeditar:
        ctk_entry_nome_do_produto_frameeditar.insert(0, recebe_dados_produto[0][0])
        ctk_entry_editarvalor_frameeditar.insert(0,recebe_dados_produto[0][1])
        textbox_editar_nome_frameeditar.insert(0.0,recebe_dados_produto[0][2])
    elif arg_scrollabelframe == scrolllabel_lista_de_produtos_framesaida:
        ctk_entry_nome_quantidade_estoque_framesaida.insert(0,recebe_dados_produto[0][0] +" | Qtd: " + str(recebe_dados_produto[0][3]))
    elif arg_scrollabelframe == scrolllabel_lista_entrada:
        ctk_entry_nome_quantidade_estoque_frameentrada.insert(0,recebe_dados_produto[0][0] +" | Qtd: " + str(recebe_dados_produto[0][3]))
    else:
        pass

def desmarcar_check_box(arg_scrollabelframe):
    if arg_scrollabelframe == scrollabel_lista_frameeditar:
        ctk_entry_nome_do_produto_frameeditar.delete(0, "end")
        ctk_entry_editarvalor_frameeditar.delete(0, "end")
        textbox_editar_nome_frameeditar.delete(0.0, "end")
    elif arg_scrollabelframe == scrolllabel_lista_de_produtos_framesaida:
        ctk_entry_nome_quantidade_estoque_framesaida.delete(0, "end")
    elif arg_scrollabelframe == scrolllabel_lista_entrada:
        ctk_entry_nome_quantidade_estoque_frameentrada.delete(0, "end")
    else:
        pass




def seleciona_item(arg_item, arg_list):
    global valor_checkbox
    valor_checkbox = arg_item.get().strip("(),'\"")
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"SELECT * FROM itens WHERE nome = '{valor_checkbox}'")
    receber_dados_produtos = terminal_sql.fetchall
    insere_dados (receber_dados_produtos,arg_list)

def deletar_produto(nome_produto):
    conexao = sqlite3.connect("dados.db")
    terminalsql = conexao.cursor()
    terminalsql.execute(f"DELETE FROM itens WHERE nome = '{nome_produto}'")
    conexao.commit()
    conexao.close()
    ctk_entry_nome_do_produto_frameeditar.delete(0, "end")
    ctk_entry_editarvalor_frameeditar.delete(0, "end")
    textbox_editar_nome_frameeditar.delete(0.0,"end")
    ler_dados_mostrar(scrollabel_lista_frameeditar)




def editar_produto(nome_produto,preco_produto,descricao_produto):
    conexao = sqlite3.connect("dados.db")
    terminalsql = conexao.cursor()
    terminalsql.execute(f"UPDATE itens SET nome = '{nome_produto}',preco = '{preco_produto}', descricao = '{descricao_produto}' WHERE nome = '{valor_checkbox.get()}")
    conexao.commit()
    conexao.close()
    ctk_entry_nome_do_produto_frameeditar.delete(0, "end")
    ctk_entry_editarvalor_frameeditar.delete(0, "end")
    textbox_editar_nome_frameeditar.delete(0.0,"end")
    ler_dados_mostrar(scrollabel_lista_frameeditar)
    
    
    

        
        






criar_banco()
# definir as funçoes para abrir e fechar o frame
def abrir_frame_cadastro():
    # fechar frames
    frame_de_editar.grid_forget()
    frame_de_saida.grid_forget()
    frame_de_entrada.grid_forget()
    frame_de_relatorio.grid_forget()
    frame_relatorio_de_saida.grid_forget()
    frame_relatorio_de_entrada.grid_forget()
    #abrir frame
    frame_cadastro.grid_propagate(False)
    frame_cadastro.grid(row=0, column=1, padx=5, pady=5)


def abrir_frame_edicao():
    frame_cadastro.grid_forget()
    frame_de_saida.grid_forget()
    frame_de_entrada.grid_forget()
    frame_de_relatorio.grid_forget()
    frame_relatorio_de_saida.grid_forget()
    frame_relatorio_de_entrada.grid_forget()
    frame_de_editar.grid_propagate(False)
    frame_de_editar.grid(row=0, column= 1,padx=5,pady=10)
    ler_dados_mostrar(scrollabel_lista_frameeditar)


def abrir_frame_saida():
    frame_cadastro.grid_forget()
    frame_de_editar.grid_forget()
    frame_de_entrada.grid_forget()
    frame_de_relatorio.grid_forget()
    frame_relatorio_de_saida.grid_forget()
    frame_relatorio_de_entrada.grid_forget()
    frame_de_saida.grid_propagate(False)
    frame_de_saida.grid(row=0, column=1, padx=5, pady=10)
    ler_dados_mostrar(scrolllabel_lista_de_produtos_framesaida)


def abrir_frame_de_entrada():
    frame_cadastro.grid_forget()
    frame_de_editar.grid_forget()
    frame_de_saida.grid_forget()
    frame_de_relatorio.grid_forget()
    frame_relatorio_de_saida.grid_forget()
    frame_relatorio_de_entrada.grid_forget()
    frame_de_entrada.grid_propagate(False)
    frame_de_entrada.grid(row=0, column=1, padx=5, pady=10)
    ler_dados_mostrar(scrolllabel_lista_entrada)


def abrir_frame_relatorio():
    frame_cadastro.grid_forget()
    frame_de_editar.grid_forget()
    frame_de_saida.grid_forget()
    frame_de_entrada.grid_forget()
    frame_relatorio_de_saida.grid_forget()
    frame_relatorio_de_entrada.grid_forget()
    frame_de_relatorio.grid_propagate(False)
    frame_de_relatorio.grid(row=0, column=1, padx=5, pady=10)
    ler_dados()

def abrir_relatorio_de_saida():
    frame_de_relatorio.grid_forget()
    frame_relatorio_de_entrada.grid_forget()
    frame_relatorio_de_saida.grid_propagate(False)
    frame_relatorio_de_saida.grid(row=0, column=1, padx=5, pady=10)

def abrir_relatorio_de_entrada():
    frame_de_relatorio.grid_forget()
    frame_relatorio_de_saida.grid_forget()
    frame_relatorio_de_entrada.grid_propagate(False)
    frame_relatorio_de_entrada.grid(row=0, column=1, padx=5, pady=10)



#abrir tela do popup exportar
popup = None

def abrir_poppup():
    global popup
    if popup is None or not popup.winfo_exists():
        popup = customtkinter.CTkToplevel()
        popup.geometry("590x380")
        popup.title("popup")


        label_relatorio = customtkinter.CTkLabel(popup,text="Escolher relatório(s):",text_color="#A8B30F")
        label_relatorio.grid(row=1,column=0,pady=20,padx=20,sticky="w")

        exportar_estoque = customtkinter.CTkCheckBox(popup, text="Exportar Estoque")
        exportar_estoque.grid(row=2, column=0,pady=20, padx=20, sticky="w")

        exportar_saida = customtkinter.CTkCheckBox(popup, text="Exportar Saída")
        exportar_saida.grid(row=3, column=0,pady=20, padx=20, sticky="w")

        exportar_entrada = customtkinter.CTkCheckBox(popup, text="Exportar Entrada")
        exportar_entrada.grid(row=4, column=0,pady=20, padx=20, sticky="w")

        #titulo escolher extenção

        label_extencao = customtkinter.CTkLabel(popup,text="Escolher extensão:",text_color="#A8B30F")
        label_extencao.grid(row=1,column=2,pady=20,padx=100,sticky="w")

        # Caixas para formatos de arquivo
        formato_word = customtkinter.CTkCheckBox(popup, text="Word")
        formato_word.grid(row=2, column=2,pady=20, padx=100, sticky="w")

        formato_pdf = customtkinter.CTkCheckBox(popup, text="PDF")
        formato_pdf.grid(row=3, column=2,pady=20, padx=100, sticky="w")

        formato_excel = customtkinter.CTkCheckBox(popup, text="Excel")
        formato_excel.grid(row=4, column=2,pady=20, padx=100, sticky="w")

        # botoes

        salvar_popup = customtkinter.CTkButton(popup,text="salvar",width=100)
        salvar_popup.grid(row=5,column=2,pady=5,padx=0,sticky="w")

        cancelar_popup = customtkinter.CTkButton(popup,text="cancelar",width=100)
        cancelar_popup.grid(row=5,column=1,pady=5,padx=20,sticky="w")

        popup.protocol("WM_DELETE_WINDOW", fechar_popup)
        popup.attributes("-topmost", 1) # garante que propup fica na frente
    else:
        popup.lift()

def fechar_popup():
    global popup
    if popup is not None:
        popup.destroy()
        popup = None

#def para mostrar voce clicou na lixeira
def on_trash_icon_click2(item_number):
    print(f"ícone de lixeira linha {item_number} clicado")



# def para a lixeira
def create_line2(text, item_number):

    label_scrolllabel_framesaida = customtkinter.CTkLabel(scrolllabelframe_framesaida, text="item 1")
    label_scrolllabel_framesaida.grid(pady=0, padx=5, row=item_number, column=0, stick="w")

    botao_de_lixeira_framesaida = customtkinter.CTkButton(scrolllabelframe_framesaida, text="🗑️", command=lambda: on_trash_icon_click(item_number), width=20)
    botao_de_lixeira_framesaida.grid(padx=0, pady=5, row=item_number, column=1, stick="e")

    scrolllabelframe_framesaida.grid_columnconfigure(0, weight=1)
    scrolllabelframe_framesaida.grid_columnconfigure(1, weight=0)

#def da lixeira entrada
def on_trash_icon_click(item_number2):
    print(f"ícone de lixeira linha {item_number2} clicado")

def create_line(text, item_number2):

    labelscrollframe_frame_entrada = customtkinter.CTkLabel(scrolllabelframe_frameentrada, text="item 1")
    labelscrollframe_frame_entrada.grid(pady=0, padx=5, row=item_number2, column=0, stick="w")

    botao_da_lixeira_frameentrada= customtkinter.CTkButton(scrolllabelframe_frameentrada, text="🗑️", command=lambda: on_trash_icon_click(item_number2), width=20)
    botao_da_lixeira_frameentrada.grid(padx=0, pady=5, row=item_number2, column=1, stick="e")

    scrolllabelframe_frameentrada.grid_columnconfigure(0, weight=1)
    scrolllabelframe_frameentrada.grid_columnconfigure(1, weight=0)





customtkinter.set_appearance_mode("Dark")

janela_principal = customtkinter.CTk()
janela_principal.geometry("800x400")
janela_principal.title("gerenciamento de maquinas agriculas")






frame_menu = customtkinter.CTkFrame(janela_principal,width=190,height=380,corner_radius=0,fg_color="Gray")
frame_menu.grid_propagate(False)
frame_menu.grid(row=0, column= 0,padx=5,pady=10)

# frame de cadastro

frame_cadastro = customtkinter.CTkFrame(janela_principal,width=590,height=380,corner_radius=0,fg_color="Gray")
frame_cadastro.grid_propagate(False)
frame_cadastro.grid(row= 0,column=1,padx=5,pady=5)

#frame da aba editar
frame_de_editar = customtkinter.CTkFrame(janela_principal,width=590,height=380,corner_radius=0,fg_color="Gray")
frame_de_editar.grid_propagate(False)

# frame de saida
frame_de_saida = customtkinter.CTkFrame(janela_principal,width=590,height=380,corner_radius=0,fg_color="Gray")
frame_de_saida.grid_propagate(False)

#frame da entrada
frame_de_entrada = customtkinter.CTkFrame(janela_principal,width=590,height=380,corner_radius=0,fg_color="Gray")
frame_de_entrada.grid_propagate(False)

#frame de relatorio
frame_de_relatorio = customtkinter.CTkFrame(janela_principal,width=590,height=380,corner_radius=0,fg_color="Gray")
frame_de_relatorio.grid_propagate(False)

# frame relatorio de saida
frame_relatorio_de_saida= customtkinter.CTkFrame(janela_principal,width=590,height=380,corner_radius=0,fg_color="Gray")
frame_relatorio_de_saida.grid_propagate(False)

#frame relatorio de entrada
frame_relatorio_de_entrada = customtkinter.CTkFrame(janela_principal,width=590,height=380,corner_radius=0,fg_color="Gray")
frame_relatorio_de_entrada.grid_propagate(False)


## titulo do menu de botoes do frame menu
label_titulo_menu = customtkinter.CTkLabel(frame_menu,text="Strawberry Management",width=100,font=("Couvier",15,"bold"),text_color="#A8B30F")
label_titulo_menu.grid(pady=35, padx=10,row=1,column=0)


#Botao para entrar na tela de cadastro do frame menu
botao_de_cadastrar_menu = customtkinter.CTkButton(frame_menu,text="Cadastrar",text_color="#A8B30F",fg_color="black",hover_color="Green",command=abrir_frame_cadastro)
botao_de_cadastrar_menu.grid(pady=5,padx=5)

#botao da aba editar do menu, do frame menu
botao_de_editar_menu = customtkinter.CTkButton(frame_menu,text="Editar",text_color="#A8B30F",fg_color="black",hover_color="Green",command=abrir_frame_edicao)
botao_de_editar_menu.grid(pady=5,padx=5)

#botao de para entrar na aba saida do frame menu
botao_de_saida_menu = customtkinter.CTkButton(frame_menu,text="Saida",text_color="#A8B30F",fg_color="black",hover_color="Green",command=abrir_frame_saida)
botao_de_saida_menu.grid(pady=5,padx=5)

# botao de entrada do frame menu
botao_de_entrada_menu = customtkinter.CTkButton(frame_menu,text="Entrada",text_color="#A8B30F",fg_color="black",hover_color="Green",command=abrir_frame_de_entrada)
botao_de_entrada_menu.grid(pady=5,padx=5)

#botao do menu que entra na aba relatorio
botao_de_relatorio_menu=customtkinter.CTkButton(frame_menu,text="Relatorio",text_color="#A8B30F",fg_color="black",hover_color="Green",command=abrir_frame_relatorio)
botao_de_relatorio_menu.grid(pady=5,padx=5)


#titulo da aba cadastro de prouto label
label_titulo_framecadastro = customtkinter.CTkLabel(frame_cadastro,text="Cadastro do Produto",font=("Couvier", 18, "bold"),text_color="#A8B30F")
label_titulo_framecadastro.grid(pady=30,padx=40,row=0,column=1)

# nome do produto do cadastro label
label_nome_do_produto_framecadastrado = customtkinter.CTkLabel(frame_cadastro,text="Nome do produto:",text_color="#A8B30F",font=("Couvier", 15, "bold"))
label_nome_do_produto_framecadastrado.grid(padx=40,row=1,column=0)

#preço para ser adicionado ao produto cadastrado
label_preco_do_produto_framecadastro = customtkinter.CTkLabel(frame_cadastro,text="Preço (R$):",text_color="#A8B30F",font=("Couvier", 15, "bold"))
label_preco_do_produto_framecadastro.grid(padx=40,row=2,column=0,sticky="ne")

# descriçao do produto cadastrado
label_descricao_do_produto_framecadastrado = customtkinter.CTkLabel(frame_cadastro,text="Descrição:",text_color="#A8B30F",font=("Couvier", 15, "bold"))
label_descricao_do_produto_framecadastrado.grid(padx=40,row=3,column=0,sticky="ne")

# digitar nome para cadastro
placeholder_digitar_nome_para_framecadastro= customtkinter.CTkEntry(frame_cadastro,placeholder_text="Digite o nome do produto:",width=300,text_color="#A8B30F")
placeholder_digitar_nome_para_framecadastro.grid(row=1,column=1,padx=5,pady=5)

#digitar preço para cadastro
ctk_entry_preco_framecadastro = customtkinter.CTkEntry(frame_cadastro,placeholder_text="00.0",width=80,text_color="#A8B30F")
ctk_entry_preco_framecadastro.grid(row=2,column=1,padx=5,pady=5,sticky="w")

# variavel para digitar a descriçao para fazer o cadastro
textbox_descricao_framecadastro= customtkinter.CTkTextbox(frame_cadastro,width=300,height=80,text_color="#A8B30F")
textbox_descricao_framecadastro.grid(row=3,column=1,sticky="")

# Salvar o cadastro do produto
botao_salvar_framecadastro = customtkinter.CTkButton(frame_cadastro,text="Salvar",width=80,text_color="#A8B30F",fg_color="black",hover_color="Green",command=salvar_dados)
botao_salvar_framecadastro.grid(row=4,column=1,pady=5,padx=5,sticky="e")


#titulo da aba editar
label_titulo_frame_frameeditar = customtkinter.CTkLabel(frame_de_editar, text="Tela de Edição de Produto", font=("Couvier", 18, "bold"), text_color="#A8B30F")
label_titulo_frame_frameeditar.grid(pady=20, padx=0, row=0, column=0,columnspan=4)

#lista da aba editar
scrollabel_lista_frameeditar = customtkinter.CTkScrollableFrame(frame_de_editar)
scrollabel_lista_frameeditar.grid(pady=0,padx=20,row=2,column=0,rowspan=4)

#procurar produto para editar
ctk_entry_pesquisa_frameeditar = customtkinter.CTkEntry(frame_de_editar,placeholder_text="pesquisar por produto",width=250)
ctk_entry_pesquisa_frameeditar.grid(row=1, column=0, pady=20, padx=20,columnspan=4,sticky="w")

# editar nome do produto
ctk_entry_nome_do_produto_frameeditar = customtkinter.CTkEntry(frame_de_editar,placeholder_text="nome do produto",width=200)
ctk_entry_nome_do_produto_frameeditar.grid(pady=0,padx=5,row=2,column=1,sticky="w",columnspan=3)

# editar valor do produto
ctk_entry_editarvalor_frameeditar = customtkinter.CTkEntry(frame_de_editar,placeholder_text="0.00",width=100)
ctk_entry_editarvalor_frameeditar.grid(padx=5,pady=0,row=3,column=1,sticky="w",columnspan=3)

#editar nome do produto
textbox_editar_nome_frameeditar = customtkinter.CTkTextbox(frame_de_editar,width=300,height=80)
textbox_editar_nome_frameeditar.grid(padx=5,pady=0,row=4,column=1,sticky="w",columnspan=3)

# botao de excluir produto
botao_excluir_produto_frameeditar=customtkinter.CTkButton(frame_de_editar, text="Excluir", width=80, fg_color=("Red"), hover_color="green",command=lambda : deletar_produto(ctk_entry_nome_do_produto_frameeditar.get()))
botao_excluir_produto_frameeditar.grid(padx=5, pady=5, row=5, column=1, stick="w")

# botao cancelar edição
botao_cancelar_frameeditar=customtkinter.CTkButton(frame_de_editar, text="Cancelar", width=80, fg_color=("black"), hover_color="green")
botao_cancelar_frameeditar.grid(padx=0, pady=5, row=5, column=2)

#botao Salvar edição
botao_salvar_frameedicao=customtkinter.CTkButton(frame_de_editar, text="Salvar", width=80, fg_color=("black"), hover_color="green")
botao_salvar_frameedicao.grid(padx=5, pady=5, row=5, column=3, stick="e")


# frame do titulo da saida
label_titulo_do_framesaida = customtkinter.CTkLabel(frame_de_saida, text="Tela de Saída", font=("Couvier", 18, "bold"), text_color="#A8B30F")
label_titulo_do_framesaida.grid(pady=0,padx=0, row=0, column=1)

#pesquisar produto para dar saida
ctk_entry_pesquisar_produto_framesaida = customtkinter.CTkEntry(frame_de_saida,placeholder_text="pesquisar Saida",width=220)
ctk_entry_pesquisar_produto_framesaida.grid(padx=20,pady=20,column=0,row=1,sticky="w")

#lista de prudutos para dar saida
scrolllabel_lista_de_produtos_framesaida = customtkinter.CTkScrollableFrame(frame_de_saida)
scrolllabel_lista_de_produtos_framesaida.grid(padx=20,pady=0,column=0,row=2,rowspan=4)

# frame para dar a quantidade de estoque (saida
ctk_entry_nome_quantidade_estoque_framesaida = customtkinter.CTkEntry(frame_de_saida,placeholder_text="nome e quantidade em estoque",width=300)
ctk_entry_nome_quantidade_estoque_framesaida.grid(padx=0,pady=0,column=1,row=1,sticky="w",columnspan=2)

# quantidade a ser retirada
ctk_entry_quantidade_framesaida = customtkinter.CTkEntry(frame_de_saida,placeholder_text="quantidade a ser retirada",width=190)
ctk_entry_quantidade_framesaida.grid(padx=0,pady=0,column=1,row=2,sticky="w")

#cancelar ação de saida
botao_cancelar_framesaida = customtkinter.CTkButton(frame_de_saida,text="cancelar",width=80,fg_color="red",hover_color="green")
botao_cancelar_framesaida.grid(padx=5,pady=5,row=5,column=1,sticky="w")

# salvar produtos saidos
botao_salvar_framesaida = customtkinter.CTkButton(frame_de_saida,text="salvar",width=80,fg_color="black",hover_color="green")
botao_salvar_framesaida.grid(padx=5,pady=5,row=5,column=2,sticky="e")

# botao para adicionar item de saida
botao_adicionaritem_framesaida=customtkinter.CTkButton(frame_de_saida, text="Adicionar item", width=50, fg_color=("black"), hover_color="#2f394a", command=lambda: create_line(item1, 1))
botao_adicionaritem_framesaida.grid(padx=0, pady=5, row=2, column=2, stick="e")

#para funcionar a lixeira
scrolllabelframe_framesaida = customtkinter.CTkScrollableFrame(frame_de_saida, height=100, width=300)
scrolllabelframe_framesaida.grid(pady=0, row=3, column=1, columnspan=2, stick="we")

'''items1 = [f"Item {i + 1}" for i in range(5)]
for i, item1 in enumerate(items1):
    create_line2(item1, i+5)'''

# titulo da entrada
label_titulo_frameentrada = customtkinter.CTkLabel(frame_de_entrada, text="Tela de Entrada", font=("Couvier", 18, "bold"), text_color="#A8B30F")
label_titulo_frameentrada.grid(pady=0,padx=0, row=0, column=1)

# fazer pesquisa no item que vc quer dar entrada
placeholder_pesquisa_frameentrada = customtkinter.CTkEntry(frame_de_entrada,placeholder_text="pesquisar produto",width=220)
placeholder_pesquisa_frameentrada.grid(padx=20,pady=20,column=0,row=1,sticky="w")

# lista de itens para que poderao dar entrada
scrolllabel_lista_entrada = customtkinter.CTkScrollableFrame(frame_de_entrada)
scrolllabel_lista_entrada.grid(padx=20,pady=0,column=0,row=2,rowspan=4)


ctk_entry_nome_quantidade_estoque_frameentrada = customtkinter.CTkEntry(frame_de_entrada,placeholder_text="nome e quantidade em estoque",width=300)
ctk_entry_nome_quantidade_estoque_frameentrada.grid(padx=0,pady=0,column=1,row=1,sticky="w",columnspan=2)



# nome e quantidade dos produtos
placeholder_quantidade_nome_frameentrada = customtkinter.CTkEntry(frame_de_entrada,placeholder_text="quantidade recebida",width=190)
placeholder_quantidade_nome_frameentrada.grid(padx=0,pady=0,column=1,row=2,sticky="w")

#cancelar ação de entrada
botao_cancelar_frameentrada = customtkinter.CTkButton(frame_de_entrada,text="cancelar",width=80,fg_color="red",hover_color="green")
botao_cancelar_frameentrada.grid(padx=5,pady=5,row=5,column=1,sticky="w")

# salvar produtos entrados
botao_salvar_frameentrada = customtkinter.CTkButton(frame_de_entrada,text="salvar",width=80,fg_color="black",hover_color="green")
botao_salvar_frameentrada.grid(padx=5,pady=5,row=5,column=2,sticky="e")

#caixinha do produto de lixeira para o frame de entrada
scrolllabelframe_frameentrada = customtkinter.CTkScrollableFrame(frame_de_entrada, height=100, width=300)
scrolllabelframe_frameentrada.grid(pady=0, row=3, column=1, columnspan=2, stick="we")

#botao de adicionar item
botao_adicionaritem_frameentrada=customtkinter.CTkButton(frame_de_entrada, text="Adicionar item", width=50, fg_color=("black"), hover_color="#2f394a", command=lambda: create_line(items1, 1))
botao_adicionaritem_frameentrada.grid(padx=0, pady=5, row=2, column=2, stick="e")

"""items2 = [f"Item {i + 1}" for i in range(5)]
for i, items2 in enumerate(items1):
    create_line(items2, i+5)"""



# titulo do relatorio
titulo_do_relatorio = customtkinter.CTkLabel(frame_de_relatorio, text="Tela de Relatório",font=("Couvier", 18, "bold"), text_color="#A8B30F")
titulo_do_relatorio.grid(pady=30,padx=30, row=0, column=0,columnspan=4)

# buscar produto do relatorio
buscar_produto_do_relatorio = customtkinter.CTkEntry(frame_de_relatorio,placeholder_text="Buscar Produto",width=220)
buscar_produto_do_relatorio.grid(column=0,row=1,padx=20,pady=20,sticky="w")

# botao para abrir popup, o botao de exportar
botao_exportar_abrir_popup = customtkinter.CTkButton(frame_de_relatorio,text="Exportar",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_poppup)
botao_exportar_abrir_popup.grid(column=3,row=1,padx=0,pady=5,sticky="w")

#tabela de table wiew estoque
tabela_table_wiew_estoque= ttk.Treeview(frame_de_relatorio,columns=("nome","quantidade","preço","descricao"),show="headings",height=5)
tabela_table_wiew_estoque.grid(row=2,padx=20,pady=5,column=0 ,columnspan=4,sticky="wsne")

#configurar tabela de table wiew estoque
tabela_table_wiew_estoque.heading("nome",text="nome")
tabela_table_wiew_estoque.heading("quantidade",text="quantidade")
tabela_table_wiew_estoque.heading("preço",text="preço")
tabela_table_wiew_estoque.heading("descricao",text="descricao")

# tamnaho da largura das colunas
tabela_table_wiew_estoque.column("nome",width=110)
tabela_table_wiew_estoque.column("quantidade",width=110)
tabela_table_wiew_estoque.column("preço",width=110)


# Criar uma barra de rolagem
scrollbar_framerelatorio = tk.Scrollbar(frame_de_relatorio, orient="vertical", command=tabela_table_wiew_estoque.yview)
scrollbar_framerelatorio.grid(row=2, column=4, sticky='ns')

#botao para entrar na aba relatorio de estoque
botao_relatorio_estoque_framerelatorio=customtkinter.CTkButton(frame_de_relatorio,text="estoque",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_frame_relatorio)
botao_relatorio_estoque_framerelatorio.grid(column=1,row=3,padx=0,pady=5,sticky="w")

#botao entrar em relatorio de saida
botao_relatorio_saida_framerelatorio = customtkinter.CTkButton(frame_de_relatorio,text="Saída",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_relatorio_de_saida)
botao_relatorio_saida_framerelatorio.grid(column=2,row=3,padx=0,pady=5,sticky="w")

#botao para entrar no relatorioo de entrada
botao_relatorio_entrada_framerelatorio=customtkinter.CTkButton(frame_de_relatorio,text="entrada",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_relatorio_de_entrada)
botao_relatorio_entrada_framerelatorio.grid(column=3,row=3,padx=0,pady=5,sticky="w")


#titulo do relatorio de saida
titulo_framerelatorio_saida = customtkinter.CTkLabel(frame_relatorio_de_saida,text="relatorio de saida",font=("Couvier", 18, "bold"), text_color="#A8B30F")
titulo_framerelatorio_saida.grid(pady=30,padx=30,row=0,column=0,columnspan=4)

#buscar produto do relatorio de saida
placeholder_pesquisa_relatorio_framesaida = customtkinter.CTkEntry(frame_relatorio_de_saida,placeholder_text="Buscar Produto",width=220)
placeholder_pesquisa_relatorio_framesaida.grid(column=0,row=1,padx=20,pady=20,sticky="w")

#botao abrir popup na aba saida
botao_exportar_framesaida = customtkinter.CTkButton(frame_relatorio_de_saida,text="Exportar",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_poppup)
botao_exportar_framesaida.grid(column=3,row=1,padx=0,pady=5,sticky="w")

#tabela table wiew saida
tabela_table_wiew_framerelatoriosaida = ttk.Treeview(frame_relatorio_de_saida,columns=("nome","quantidade","Data/hora"),show="headings",height=5)
tabela_table_wiew_framerelatoriosaida.grid(row=2,padx=20,pady=5,column=0 ,columnspan=4,sticky="wsne")

#configurar tabela do table wiew saida
tabela_table_wiew_framerelatoriosaida.heading("nome",text="nome")
tabela_table_wiew_framerelatoriosaida.heading("Data/hora",text="Data/hora")
tabela_table_wiew_framerelatoriosaida.heading("quantidade",text="quantidade")
#configurar tamanho da coluna
tabela_table_wiew_framerelatoriosaida.column("nome",width=178)
tabela_table_wiew_framerelatoriosaida.column("quantidade",width=178)
tabela_table_wiew_framerelatoriosaida.column("Data/hora",width=178)

# Adicionar linhas vazias table wiew saida
for _ in range(10):  # Adiciona 10 linhas vazias
    tabela_table_wiew_framerelatoriosaida.insert("", "end", values=("", "", "", ""))

# Criar uma barra de rolagem
scrollbar_framerelatoriosaida = tk.Scrollbar(frame_relatorio_de_saida, orient="vertical", command=tabela_table_wiew_framerelatoriosaida.yview)
scrollbar_framerelatoriosaida.grid(row=2, column=4, sticky='ns')

#botao entrar no estoque relatorio
boatao_estoque_framerelatoriosaida = customtkinter.CTkButton(frame_relatorio_de_saida,text="estoque",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_frame_relatorio)
boatao_estoque_framerelatoriosaida.grid(column=1,row=3,padx=0,pady=5,sticky="w")

# botao entrar no relatorio de saida
botao_saida_framerelatoriosaida = customtkinter.CTkButton(frame_relatorio_de_saida,text="Saída",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_relatorio_de_saida)
botao_saida_framerelatoriosaida.grid(column=2,row=3,padx=0,pady=5,sticky="w")

#botao entrada de relatorio
botao_entrada_framerelatoriosaida = customtkinter.CTkButton(frame_relatorio_de_saida,text="entrada",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_relatorio_de_entrada)
botao_entrada_framerelatoriosaida.grid(column=3,row=3,padx=0,pady=5,sticky="w")

#titulo do relatorio de entrada
titulo_do_relatorio_frameentrada = customtkinter.CTkLabel(frame_relatorio_de_entrada,text="relatorio de entrada",font=("Couvier", 18, "bold"), text_color="#A8B30F")
titulo_do_relatorio_frameentrada.grid(pady=30,padx=30,row=0,column=0,columnspan=4)

#buscar produto no relatorio de entrada
placeholder_pesquisa_framerelatorio_entrada = customtkinter.CTkEntry(frame_relatorio_de_entrada,placeholder_text="Buscar Produto",width=220)
placeholder_pesquisa_framerelatorio_entrada.grid(column=0,row=1,padx=20,pady=20,sticky="w")

# abrir popup relatorio de entrada
botao_exportar_framerelatorioentrada = customtkinter.CTkButton(frame_relatorio_de_entrada,text="Exportar",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_poppup)
botao_exportar_framerelatorioentrada.grid(column=3,row=1,padx=0,pady=5,sticky="w")

#tabela table wiew entrada
tabela_table_wiew_framerelatorioentrada = ttk.Treeview(frame_relatorio_de_entrada,columns=("nome","quantidade","Data/hora"),show="headings",height=5)
tabela_table_wiew_framerelatorioentrada.grid(row=2,padx=20,pady=5,column=0 ,columnspan=4,sticky="wsne")

#configurar tabela do de entrada
tabela_table_wiew_framerelatorioentrada.heading("nome",text="nome")
tabela_table_wiew_framerelatorioentrada.heading("Data/hora",text="Data/hora")
tabela_table_wiew_framerelatorioentrada.heading("quantidade",text="quantidade")
#configurar o tamnaho da tabela
tabela_table_wiew_framerelatorioentrada.column("nome",width=178)
tabela_table_wiew_framerelatorioentrada.column("quantidade",width=178)
tabela_table_wiew_framerelatorioentrada.column("Data/hora",width=178)

# Adicionar linhas vazias
for _ in range(10):  # Adiciona 10 linhas vazias
    tabela_table_wiew_framerelatorioentrada.insert("", "end", values=("", "", "", ""))

# Criar uma barra de rolagem para o table view da entrada
scrollbar_frameentrada_entrada = tk.Scrollbar(frame_relatorio_de_entrada, orient="vertical", command=tabela_table_wiew_framerelatorioentrada.yview)
scrollbar_frameentrada_entrada.grid(row=2, column=4, sticky='ns')

#botao estoque entrada
botao_estoque_frameentrada=customtkinter.CTkButton(frame_relatorio_de_entrada,text="estoque",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_frame_relatorio)
botao_estoque_frameentrada.grid(column=1,row=3,padx=0,pady=5,sticky="w")

#botao entar no relatorio saida
botao_de_saida_frameentrada = customtkinter.CTkButton(frame_relatorio_de_entrada,text="Saída",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_relatorio_de_saida)
botao_de_saida_frameentrada.grid(column=2,row=3,padx=0,pady=5,sticky="w")

# botao de entrar na entrada
botao_entrada_frameentrada=customtkinter.CTkButton(frame_relatorio_de_entrada,text="entrada",width=80,fg_color=("black"), hover_color="#2f394a",command=abrir_relatorio_de_entrada)
botao_entrada_frameentrada.grid(column=3,row=3,padx=0,pady=5,sticky="w")

janela_principal.mainloop()