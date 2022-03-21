#!/usr/bin/python3
#
#
#       ########################################################################
#       #       Virifica Replicador de Tira Teima e exporta em arquivo .txt    #
#       #       Versão 1.6                                                     #
#       #       Data 13/01/2021                                                #
#       #       By_Anderson Galdino                                            #
#       ########################################################################
#
#
#
#   **** Os dados da empresa foram alterado para manter o sigilo    ****
#
#
import os
import time
import DB
import subprocess


class c_style:
    S_HEADER = '\033[31m'
    S_END = '\033[0m'
    S_GREEN = '\033[92m'
    S_YELLOW = '\033[93m'
    S_BLUE = '\033[94m'
    S_RED = '\033[91m'


def validacaoRede():
    ip = "10.%s.2.%s" % (filial, pdv)
    print(c_style.S_BLUE + 'PDV: %s' % pdv + c_style.S_END)
    valida1 = (subprocess.getoutput("ssh %s netstat -ntu | grep 6500" % ip))
    valida2 = (subprocess.getoutput("ssh %s netstat -ntu | grep 1007" % ip))

    if (ip + ":6500") in valida1:
        print(c_style.S_HEADER + 'PDV %s > Replicador' % pdv + c_style.S_END)
        print(valida1)

        with open(arquivo0, 'a') as saida:
            saida.write(str(filial) + '_' + (nome_Filial[filial]) + '_PDV:')
            saida.write(str(pdv) + '\n' + valida1 + '\n\n')

    elif (ip + ":1007") in valida2:
        print(c_style.S_HEADER + 'PDV %s > Replicador' % pdv + c_style.S_END)
        print(valida2)

        with open(arquivo0, 'a') as saida:
            saida.write(str(filial) + '_' + (nome_Filial[filial]) + '_PDV:')
            saida.write(str(pdv) + '\n' + valida2 + '\n\n')
    return ()


def validacaoFilial():
    ip = "10.%s.2.%s" % (filial, pdv)
    print(c_style.S_BLUE + 'PDV: %s' % pdv + c_style.S_END)
    valida1 = (subprocess.getoutput("ssh %s netstat -ntu | grep 6500" % ip))
    valida2 = (subprocess.getoutput("ssh %s netstat -ntu | grep 1007" % ip))

    if (ip + ":6500") in valida1:
        print(c_style.S_HEADER + 'PDV %s > Replicador' % pdv + c_style.S_END)
        print(valida1)

    elif "1007" in valida2:
        print(c_style.S_HEADER + 'PDV %s > Replicador' % pdv + c_style.S_END)
        print(valida2)

    return ()


# Numero das Filiais Muffato e Max
num_F_Geral = DB.filialVAREJO + DB.filialMAX

# Nome de cada Filial sendo= 'Filial 1':'nome', 'Filial 2':'nome'...
nome_Filial = DB.nomeFilial

# Quantidade de PDVs em cada Filial sendo= 'Filial 1':'quantidade de PDV', 'Filial 2':'quantidade de PDV'...
quant_PDV = DB.quantPDV

os.system("clear")
print(c_style.S_HEADER + ' ************************************************************************** \n'
                         ' ********      Verificar os PDVs Replicadores de Titra Teimas      ******** \n'
                         ' ********                  By_Anderson Galdino                     ******** \n'
                         ' ************************************************************************** \n' + c_style.S_END)

indicefilial = 0

dia = str(time.localtime()[2])
mes = str(time.localtime()[1])
ano = str(time.localtime()[0])
data = str(dia + mes + ano)
arquivo0 = 'Replicadores' + '_' + dia + '_' + mes + '_' + ano + '.txt'

escolha = (input(c_style.S_YELLOW + 'Onde deseja executar:\n'
                                    '  1=Escolher a filial..........2=Rede MAX\n'
                                    '  3=Rede Varejo................4=Toda a Rede\n:> ' + c_style.S_END))

while '1' != escolha != '2' and '3' != escolha != '4':
    print(c_style.S_RED + 'Digito invalido!' + c_style.S_END)
    escolha = (input(c_style.S_YELLOW + 'Onde deseja executar:\n '
                                        '1=Escolher a filial              2=Rede MAX\n'
                                        '3=Rede Varejo                    4=Toda a Rede\n:> ' + c_style.S_END))

if escolha == '1':

    # solicita o numero da filial
    filial = str(input(c_style.S_BLUE + 'Informe o numero da Filial:\n> '))

    while filial not in num_F_Geral:
        print(c_style.S_RED + 'Filial invalida...' + c_style.S_END)
        filial = str(input(c_style.S_BLUE + 'Informe o numero correto da Filial:\n> '))

    while filial != 0:
        nome_Filial = DB.nomeFilial
        print(c_style.S_GREEN + "Loja: " + nome_Filial[filial] + c_style.S_END)
        # Defina o PDV
        pdv = 101
        quantpdv = int(quant_PDV[filial])
        print(c_style.S_GREEN + 'Analisando a Filial: %s %s' % (filial, nome_Filial[filial]) + c_style.S_END)

        for p in range(quantpdv):
            validacaoFilial()
            pdv += 1

        filial = 0
elif escolha == '2':
    var_range = len(DB.filialMAX)
    for i in range(var_range):
        pdv = 101
        filial = DB.filialMAX[indicefilial]
        quantpdv = int(quant_PDV[filial])
        print(c_style.S_GREEN + 'Analisando a Filial: %s %s' % (filial, nome_Filial[filial]) + c_style.S_END)

        for p in range(quantpdv):
            validacaoRede()
            pdv += 1

        indicefilial += 1

elif escolha == '3':
    var_range = len(DB.filialVAREJO)
    for i in range(var_range):
        pdv = 101
        filial = DB.filialVAREJO[indicefilial]
        quantpdv = int(quant_PDV[filial])
        print(c_style.S_GREEN + 'Analisando a Filial: %s %s' % (filial, nome_Filial[filial]) + c_style.S_END)

        for p in range(quantpdv):
            validacaoRede()
            pdv += 1

        indicefilial += 1

elif escolha == '4':
    var_range = len(DB.filialVAREJO + DB.filialMAX)
    for i in range(var_range):
        pdv = 101
        filial = num_F_Geral[indicefilial]
        quantpdv = int(quant_PDV[filial])
        print(c_style.S_GREEN + 'Analisando a Filial: %s %s' % (filial, nome_Filial[filial]) + c_style.S_END)

        for p in range(quantpdv):
            validacaoRede()
            pdv += 1

        indicefilial += 1

print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Fim do Processo              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)
