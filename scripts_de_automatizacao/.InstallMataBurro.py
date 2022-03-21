#!/usr/bin/python3
#
#
#       ###############################################
#       #       Transformar PDV em Mata Burro         #
#       #       Versão 1.2                            #
#       #       Data 14/01/2021                       #
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


class c_style:
    S_HEADER = '\033[31m'
    S_BLUE = '\033[94m'
    S_GREEN = '\033[92m'
    S_YELLOW = '\033[93m'
    S_RED = '\033[91m'
    S_END = '\033[0m'


os.system("clear")
print(c_style.S_HEADER + ' ******************************************************* \n'
                         ' ********     Transformar PDV em Mata Burro     ******** \n'
                         ' ********          By_Anderson Galdino          ******** \n'
                         ' ******************************************************* \n')

filialGERAL = DB.filialVAREJO + DB.filialMAX
# solicita o numero da filial
filial = int(input(c_style.S_BLUE + 'Informe o numero da Filial:\n> ' + c_style.S_END))
filial = str(filial)
while filial not in filialGERAL:
    print(c_style.S_RED + 'Filial invalida...')
    filial = int(input(c_style.S_BLUE + 'Informe o numero correto da Filial:\n> ' + c_style.S_END))
    filial = str(filial)

while filial != 0:
    print(c_style.S_GREEN + "Loja: " + DB.nomeFilial[filial])
    # solicita o PDV para Transformação
    pdv = int(input(c_style.S_BLUE + 'Informe o numero do PDV para transformar:\n> ' + c_style.S_END))

    if pdv < 100:
        pdv = pdv + 100
        print(c_style.S_GREEN + 'PDV: %s' % pdv)
    else:
        print(c_style.S_GREEN + 'PDV: %s' % pdv)

    ip = '10.%s.2.%s' % (filial, pdv)
    print(c_style.S_YELLOW + "Copiando arquivos...")
    os.system("scp rc.modules %s:/etc/rc.d/" % ip)
    os.system("scp rc.modules.local %s:/etc/rc.d/" % ip)
    os.system("scp rc.local %s:/etc/rc.d/" % ip)
    os.system("scp PosId %s:/var/venditor/PRM/" % ip)
    print(c_style.S_BLUE + "Fim da Copia de arquivos.")
    print(c_style.S_HEADER + "Iniciando Configuracao de Rede do Mata Burro:")
    input(c_style.S_RED + "Pressione ENTER para continuar")
    os.system("ssh root@%s -t netconfig" % ip)
    os.system("scp resolv.conf %s:/etc/" % ip)
    print(c_style.S_GREEN + "Reiniciando a Maquina\n\n")
    os.system("ssh %s 'init 6'" % ip)
    print(c_style.S_RED + "*****      ENVIAR CARGA DO EMPORIUM     *****\n")
    print(c_style.S_GREEN + "*****             PLU Geral             *****\n"
                            "*****         Complemento de PLU        *****\n"
                            "*****              Clientes             *****\n"
                            "*****        Complemento Clientes       *****\n"
                            "*****              Usuarios             *****\n"
                            "***** Programa, temas, parametros, etc. *****\n")

    filial = 0

print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Fim do Processo              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)
