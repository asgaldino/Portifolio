#
#
#
#                   #####################################
#                   #   Sistema de Registro de Ponto    #
#                   #   By_Anderson Galdino             #
#                   #   Versão 1.0                      #
#                   #####################################

import PySimpleGUI as psg


# Criano função da interface grafica da primeira tela
def home():
    psg.theme('Reddit')
    # define a variavel do layout
    homelayout = [
        # cria os itens da tela com seus atributos
        [psg.Text('Entre com os dados para Registro')],
        [psg.Text('CPF'), psg.Input(key='cpf', size=(12, 1))],
        [psg.Text('Senha'), psg.Input(key='senha', password_char='*', size=(5, 1))],
        [psg.Button('Cancelar'), psg.Button('Registrar')]
    ]
    # Define variavel da janela com seus atributos e linca com o layout
    window = psg.Window('Registro de Ponto', homelayout, size=(300, 120), element_justification='center')
    # define variavel de ações para os botões
    button, values = window.read()
    # Define condicional para cada botão
    if button == 'Registrar':
        window.close()
        # Condicional de verificação de usuário e senha *** Integrar com o Banco de dados ***
        if values['cpf'] == '00123456789' and values['senha'] == '123456':
            confirmation()
        else:
            errorwindow()
    if button == 'Cancelar':
        exit()
    if button == psg.WINDOW_CLOSED:
        exit()


def confirmation():
    psg.theme('DarkGreen5')
    conflayout = [
        [psg.Text('Registrado com Sucesso')],
        [psg.Button('OK')]
    ]
    window1 = psg.Window('Registrado com Sucesso', conflayout, size=(200, 80), element_justification='center')
    button, values = window1.Read()
    if button == 'OK':
        exit()
    if button == psg.WINDOW_CLOSED:
        exit()


def errorwindow():
    psg.theme('DarkRed1')
    errorlayout = [
        [psg.Text('Dados Incorretos')],
        [psg.Button('Cancelar'), psg.Button('Tentar Novamente')]
    ]
    window2 = psg.Window('Dados Incorretos', errorlayout, size=(250, 80), element_justification='center')
    button, values = window2.Read()
    if button == 'Tentar Novamente':
        window2.close()
        home()
    if button == 'Cancelar':
        exit()
    if button == psg.WINDOW_CLOSED:
        exit()


home()
