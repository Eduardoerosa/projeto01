import os

# ================================
# Base de dados em memória
# ================================
restaurantes = [
    {'nome': 'Praça', 'categoria': 'Japonesa', 'ativo': False},
    {'nome': 'Pizza Suprema', 'categoria': 'Pizza', 'ativo': True},
    {'nome': 'Cantina', 'categoria': 'Italiano', 'ativo': False}
]

# ================================
# Utilidades de interface
# ================================

def limpar_tela():
    '''
    Docstring para limpar_tela
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_subtitulo(texto):
    '''
    Docstring for exibir_subtitulo
    
    :param texto: Description
    '''
    limpar_tela()
    linha = '*' * len(texto)
    print(linha)
    print(texto)
    print(linha)
    print()


def voltar_menu_principal():
    '''
    Docstring for voltar_menu_principal
    '''
    input('\nPressione ENTER para voltar ao menu...')
    main()

# ================================
# Funcionalidades
# ================================

def cadastrar_novo_restaurante():
    '''
    Docstring for cadastrar_novo_restaurante
    inputs para o nome do restaurante
    '''
    
    exibir_subtitulo('Cadastro de novos restaurantes')
    nome_do_restaurante = input('Digite o nome do restaurante: ')
    categoria = input(f'Digite a categoria do restaurante {nome_do_restaurante}: ')

    dados_do_restaurante = {
        'nome': nome_do_restaurante,
        'categoria': categoria,
        'ativo': False
    }

    restaurantes.append(dados_do_restaurante)

    print(f"\nO restaurante {nome_do_restaurante} foi cadastrado com sucesso!")
    voltar_menu_principal()



def listar_restaurantes():

    '''
    Docstring for listar_restaurantes
    '''
    exibir_subtitulo('Listando restaurantes')

    print(f"{'Nome do restaurante'.ljust(22)} | {'Categoria'.ljust(20)} | Status")
    print('-' * 60)

    for restaurante in restaurantes:
        nome_restaurante = restaurante['nome']
        categoria = restaurante['categoria']
        ativo = 'ativado' if restaurante['ativo'] else 'desativado'
        print(f"- {nome_restaurante.ljust(20)} | {categoria.ljust(20)} | {ativo}")

    voltar_menu_principal()



def alternar_estado_restaurante():
    '''
    Docstring for alternar_estado_restaurante
    '''
    exibir_subtitulo('Alterando estado do restaurante')
    nome_restaurante = input('Digite o nome do restaurante que deseja alterar o estado: ')

    restaurante_encontrado = False

    for restaurante in restaurantes:
        if nome_restaurante == restaurante['nome']:
            restaurante_encontrado = True
            restaurante['ativo'] = not restaurante['ativo']

            mensagem = (
                f'O restaurante {nome_restaurante} foi ativado com sucesso!'
                if restaurante['ativo']
                else f'O restaurante {nome_restaurante} foi desativado com sucesso!'
            )
            print(mensagem)

    if not restaurante_encontrado:
        print('O restaurante não foi encontrado.')

    voltar_menu_principal()



def finalizar_app():
    '''
    Docstring for finalizar_app
    '''
    exibir_subtitulo('Finalizando aplicação')
    print('Aplicação encerrada. Até logo!')
    exit()


# ================================
# Menu
# ================================

def exibir_opcoes():
    '''
    Docstring for exibir_opcoes
    '''
    print('1. Cadastrar restaurante')
    print('2. Listar restaurantes')
    print('3. Alternar estado do restaurante')
    print('4. Sair\n')



def escolher_opcao():
    '''
    Docstring for escolher_opcao
    '''
    try:
        opcao_escolhida = int(input('Escolha uma opção: '))

        if opcao_escolhida == 1:
            cadastrar_novo_restaurante()
        elif opcao_escolhida == 2:
            listar_restaurantes()
        elif opcao_escolhida == 3:
            alternar_estado_restaurante()
        elif opcao_escolhida == 4:
            finalizar_app()
        else:
            print('Opção inválida!')
            voltar_menu_principal()
    except ValueError:
        print('Digite apenas números!')
        voltar_menu_principal()


# ================================
# App principal
# ================================

def main():
    '''
    Docstring for main
    '''
    limpar_tela()
    print('=== Sistema de Restaurantes ===\n')
    exibir_opcoes()
    escolher_opcao()


if __name__ == '__main__':
    
    main()
