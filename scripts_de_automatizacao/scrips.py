#!/usr/bin/python3
#
#

import os


# Define variaveis de estilo
class c_style:
    S_HEADER = '\033[31m'
    S_END = '\033[0m'
    S_GREEN = '\033[92m'
    S_YELLOW = '\033[93m'
    S_BLUE = '\033[94m'


os.system("clear")

print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Menu de Scripts              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)

print(c_style.S_GREEN +
      '***********************************...Menu...***********************************\n\n' + c_style.S_END)
print(c_style.S_YELLOW +
      '  1 = Verifica Replicador         2 = Instalar Gate-Cach          3 = Configura PC de Etiquetas\n'
      '  4 = Gera-Pedido Varejo          5 = Linkar SAT                  6 = Instalar QR Code\n'
      '  7 = Instalar SAT                8 = Instalar Mata-Burro         9 = Instalar Impressora\n'
      ' 10 = Busca SATs Linkados\n\n' + c_style.S_END)

menu = input(c_style.S_BLUE + "Escolua um Scrypt do menu:\n :>  " + c_style.S_END)

if menu == '1':
    os.system('./.VerificaReplicadorTT.py')
    exit()

elif menu == '2':
    os.system('./.InstallGateCach.py')
    exit()

elif menu == '3':
    os.system('./.PCetiquetas.py')
    exit()

elif menu == '4':
    os.system('./.GeraPedidoVarejo.py')
    exit()

elif menu == '5':
    os.system('./.linkarSAT.py')
    exit()

elif menu == '6':
    os.system('./.InstallQRcode.py')
    exit()

elif menu == '7':
    os.system('./.InstallSAT.py')
    exit()

elif menu == '8':
    os.system('./.InstallMataBurro.py')
    exit()

elif menu == '9':
    os.system('./.installNFCE_Varejo.py')
    exit()

elif menu == '10':
    os.system('./.buscaSATsLinkados.py')
    exit()
