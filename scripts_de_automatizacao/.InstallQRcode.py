#!/usr/bin/python3
#
#
#       ###############################################
#       #       Instala QRcode Para Pagamentos        #
#       #       Versão 1.2                            #
#       #       Data 19/01/2021                       #
#       #       By_Anderson Galdino                   #
#       ###############################################
#
#
#
#   **** Os dados da empresa foram alterado para manter o sigilo    ****
#
#
import os
import DB


class s_style:
    S_HEADER = '\033[31m'
    S_BLUE = '\033[94m'
    S_GREEN = '\033[92m'
    S_YELLOW = '\033[93m'
    S_RED = '\033[91m'
    S_END = '\33[0m'


os.system("clear")
print(s_style.S_HEADER + ' ************************************************************************ \n'
                         ' ********                   Instalar QRcode                      ******** \n'
                         ' ********                  By_Anderson Galdino                   ******** \n'
                         ' ************************************************************************ \n' + s_style.S_END)

filial_GERAL = DB.filialVAREJO + DB.filialMAX + DB.filialPOSTO
# solicita o numero da filial
filial = str(input(s_style.S_YELLOW + 'Informe o numero da Filial:\n> ' + s_style.S_END))

while filial not in filial_GERAL:
    print(s_style.S_RED + 'Filial invalida...' + s_style.S_END)
    filial = str(input(s_style.S_YELLOW + 'Informe o numero correto da Filial:\n> ' + s_style.S_END))

while filial != 0:
    print(s_style.S_GREEN + "Loja: " + DB.nomeFilial[filial] + s_style.S_END)
    # Defina o PDV
    # solicita o PDV para Transformação
    pdv = int(input(s_style.S_YELLOW + 'Informe o numero do PDV para instalar:\n> ' + s_style.S_END))

    if pdv < 100:
        pdv = pdv + 100
        print(s_style.S_GREEN + 'PDV: %s' % pdv)
    else:
        print(s_style.S_GREEN + 'PDV: %s' % pdv)

    ip = '10.%s.2.%s' % (filial, pdv)
    # Auto Posto
    if filial == "800":
        ip = "10.250.2.%s" % pdv
    elif filial == "900":
        ip = "10.245.101.%s" % pdv
    elif filial == "920":
        ip = "10.252.101.%s" % pdv

    print(s_style.S_BLUE + 'Copiando arquivos...' + s_style.S_END)
    os.system('scp -r pacotes_142/ %s:/tmp/' % ip)
    print(s_style.S_GREEN + 'Fim da copia de arquivos...' + s_style.S_END)
    print(s_style.S_BLUE + 'Instalando pacotes...' + s_style.S_END)
    os.system("ssh %s 'installpkg /tmp/pacotes_142/*.txz'" % ip)
    print(s_style.S_GREEN + 'Fim da Instalacao de pacotes...')
    input(s_style.S_YELLOW + "Pressione enter para reiniciar o Venditor." + s_style.S_END)
    os.system("ssh %s 'killall -9 venditor'" % ip)
    os.system("ssh %s 'killall -9 venditorX'" % ip)

    filial = 0

print(s_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Fim do Processo              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + s_style.S_END)
