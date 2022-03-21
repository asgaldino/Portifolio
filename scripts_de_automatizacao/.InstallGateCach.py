#!/usr/bin/python3
#
#       ###############################################
#       #       Vincula o PDV ao sistema Gate-Cach    #
#       #       Versão 1.2                            #
#       #       Data 13/11/2021                       #
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
    S_END = '\033[0m'
    S_RED = '\033[91m'


os.system("clear")
print(c_style.S_HEADER + '************************************************************ \n'
                         '********         Instalador do Gate-Cach            ******** \n'
                         '********           By_Anderson Galdino              ******** \n'
                         '************************************************************ \n' + c_style.S_END)

# solicita o numero da filial
filial = str(input(c_style.S_BLUE + 'Informe o numero da Filial:\n> '))

while filial not in DB.filialMAX:
    print(c_style.S_RED + 'Filial invalida...' + c_style.S_END)
    filial = str(input(c_style.S_BLUE + 'Informe o numero correto da Filial:\n> '))

# Defina o PDV
pdv = int(input(c_style.S_BLUE + 'Informe PDV:\n> ' + c_style.S_END))

# Trata o numero de PDV (final do IP)
if int(pdv) > 100:
    pdv = str(pdv)
else:
    pdv = str(100 + pdv)
# Define o IP
ip = "10.%s.2.%s" % (filial, pdv)

# Copia arquivos
print(c_style.S_GREEN + 'Copiando arquivos...' + c_style.S_END)

pdv = int(pdv)
if pdv <= 116:
    pdv = str(pdv)
    os.system("ssh %s 'echo Address=10.%s.50.20 > /var/venditor/PRM/gcecho.config'" % (ip, filial))
    print(c_style.S_GREEN + "Criado arquivo gcecho.config com '10.%s.50.20'" % filial + c_style.S_END)
elif pdv > 116:
    pdv = str(pdv)
    os.system("ssh %s 'echo Address=10.%s.50.21 > /var/venditor/PRM/gcecho.config'" % (ip, filial))
    print(c_style.S_GREEN + "Criado arquivo gcecho.config com '10.%s.50.21'" % filial + c_style.S_END)

os.system("scp /home/arquivos/gatecach/run_gc.sh %s:/var/venditor/bin/" % ip)
os.system("scp /home/arquivos/gatecach/libGCPlug.so %s:/usr/lib/" % ip)
os.system("scp /home/arquivos/gatecach/inittab %s:/etc/" % ip)
print(c_style.S_GREEN + 'Fim da copia dos arquivos!' + c_style.S_END)
print(c_style.S_GREEN + 'Subindo Servico...' + c_style.S_END)
os.system("ssh %s '/var/venditor/bin/run_gc.sh'" % ip)

print(c_style.S_HEADER + '************************************************************ \n'
                         '********               Fim do Processo              ******** \n'
                         '********             By_Anderson Galdino!           ******** \n'
                         '************************************************************ \n' + c_style.S_END)
