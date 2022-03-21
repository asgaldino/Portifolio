#!/usr/bin/python3
#
#
#       ##############################################################
#       #       Atualiza as bibliotecas dos SATs Tanca e Sweda       #
#       #       Versão 1.3                                           #
#       #       Data 27/09/2021                                      #
#       #       By_AndersonGaldino                                   #
#       ##############################################################
#
#
#
#   **** Os dados da empresa foram alterado para manter o sigilo    ****
#
#
import os
import DB


# Define estilos para o script
class c_style:
    S_HEADER = '\033[31m'
    s_BLUE = '\033[94m'
    s_GREEN = '\033[92m'
    s_YELLOW = '\033[93m'
    s_RED = '\033[91m'
    s_END = '\033[0m'


os.system("clear")
print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********         Automatizacao de lib SAT           ******** \n'
                         ' ************************************************************ \n' + c_style.s_END)

# solicita o numero da filial
filial = str(input(c_style.s_BLUE + 'Informe o numero da Filial:\n> ' + c_style.s_END))
while filial not in DB.filialSP:
    print(c_style.s_RED + 'Filial invalida...')
    filial = str(input(c_style.s_BLUE + 'Informe o numero correto da Filial:\n> ' + c_style.s_END))

if filial in DB.filialSP:
    print(c_style.s_GREEN + "Loja: " + DB.nomeFilial[filial] + c_style.s_END)
    # Defina o PDV
    pdv = int(input(c_style.s_BLUE + 'Informe o PDV:\n> ' + c_style.s_END))

    if pdv < 100:
        pdv = pdv + 100
        pdv = str(pdv)
        print(c_style.s_GREEN + 'PDV: %s' % pdv + c_style.s_END)
    else:
        pdv = str(pdv)
        print(c_style.s_GREEN + 'PDV: %s' % pdv + c_style.s_END)

    ip = "10.%s.2.%s" % (filial, pdv)

    print(c_style.s_YELLOW + 'Copiando Lib...' + c_style.s_END)

    os.system("ssh %s 'rm /usr/lib/libsatTANCA.so'" % ip)
    os.system("ssh %s 'rm /var/venditor/bin/libsat_v2_0_0_1_x86.so'" % ip)
    os.system("ssh %s 'rm /usr/lib/libsat_v2_0_0_1_x86.so'" % ip)

    os.system("scp libsat_v3_0_0_3_x86.so %s:/var/venditor/bin/" % ip)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/libsat_v3_0_0_3_x86.so'" % ip)
    os.system("scp libsat_v3_0_0_3_x86.so %s:/usr/lib/" % ip)
    os.system("ssh %s 'chmod 777 /usr/lib/libsat_v3_0_0_3_x86.so'" % ip)
    os.system("ssh %s 'ln -s /usr/lib/libsat_v3_0_0_3_x86.so /usr/lib/libsatTANCA.so'" % ip)

    os.system("scp libSAT.so %s:/var/venditor/bin/" % ip)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/libSAT.so'" % ip)
    os.system("scp libSAT.so %s:/usr/lib/" % ip)
    os.system("ssh %s 'chmod 777 /usr/lib/libSAT.so'" % ip)

print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Fim do Processo              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + c_style.s_END)
