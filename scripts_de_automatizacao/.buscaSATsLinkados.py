#!/usr/bin/python3
#
#       #########################################################################
#       #       Valida se os SATs estão linkados e exporta em arquivo .txt      #
#       #       Versão 1.8                                                      #
#       #       Data 27/12/2020                                                 #
#       #       By_Anderson Galdino                                             #
#       #########################################################################
#
#
#
#   **** Os dados da empresa foram alterado para manter o sigilo    ****
#
#
import os
import DB
import time
import subprocess


class c_style:
    S_HEADER = '\033[31m'
    S_BLUE = '\033[94m'
    S_GREEN = '\033[92m'
    S_WARNING = '\033[93m'
    S_END = '\033[0m'


indicefilial = 0

dia = str(time.localtime()[2])
mes = str(time.localtime()[1])
ano = str(time.localtime()[0])
data = str(dia + mes + ano)

# Numero das Filiais
filiais = DB.filialSP

# Nome das Filiais
nome = DB.nomeFilial

# quantidade de PDVs em cada Filial
quantPDV = DB.quantPDV

os.system("clear")
print(c_style.S_HEADER + ' ************************************************************* \n'
                         ' ********          Automatizacao de processo          ******** \n'
                         ' ********     Validar quais SATs estao Linkados       ******** \n'
                         ' ************************************************************* \n' + c_style.S_END)


def validacao():
    ip = "10.%s.2.%s" % (filial, pdv)
    print(c_style.S_BLUE + 'PDV: %s' % pdv)
    valida = (subprocess.getoutput("ssh %s \"sed -n '/<SND_IP/p' /var/venditor/PRM/SAT.xml\"" % ip))
    if valida == "<SND_IP>127.0.0.1</SND_IP>":
        print(c_style.S_HEADER + 'Linkado')
        ibox = (subprocess.getoutput("ssh %s \"sed -n '/<IBOX_IP/P' /var/ipos/PRM/SAT.xml\"" % ip))

        if menu == '2':
            tipo = 'Geral'
        else:
            tipo = filial
        arquivo = 'linkados' + '_' + tipo + '_' + dia + '_' + mes + '_' + ano + '.txt'
        with open(arquivo, 'a') as saida:
            saida.write(str(filial) + '_' + (nome[filial]) + '_')
            saida.write(str(pdv) + ibox + '\n')
    return ()


menu = str(input(c_style.S_WARNING + "Escolha executar em toda rede ou selecione apenas uma filial:\n"
                                     "1 = Escolher uma Filial      2 = Rodar em toda rede\n:>" + c_style.S_END))
while menu != '1' and menu != '2':
    print(c_style.S_HEADER + 'Opcao invalida...')
    menu = str(input(c_style.S_WARNING + "Escolha executar em toda rede ou selecione apenas uma filial:\n"
                                         "1 = Escolher uma Filial      2 = Rodar em toda rede\n:>" + c_style.S_END))

if menu == '2':

    for i in range(11):
        pdv = 101
        filial = filiais[indicefilial]
        quantpdv = int(quantPDV[filial])
        print(c_style.S_GREEN + 'Analisando a Filial: %s %s' % (filial, nome[filial]) + c_style.S_END)

        for p in range(quantpdv):
            validacao()
            pdv += 1

        indicefilial += 1
else:
    filial = str(input(c_style.S_BLUE + 'Informe o numero da Filial:\n> ' + c_style.S_END))

    while filial not in filiais:
        print(c_style.S_HEADER + 'Opcao invalida...')
        filial = str(input(c_style.S_BLUE + 'Informe o numero correto da Filial:\n> ' + c_style.S_END))

    pdv = 101
    quantpdv = int(quantPDV[filial])
    print(c_style.S_GREEN + 'Analisando a Filial: %s %s' % (filial, nome[filial]) + c_style.S_END)

    for p in range(quantpdv):
        validacao()
        pdv += 1

print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Fim do Processo              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)
