#!/usr/bin/python3
#
#
#       ###############################################
#       #       Gera Pedido No SAP (Cockpit)          #
#       #       Versão 1.5                            #
#       #       Data 23/01/2021                       #
#       #       By_Anderson Galdino                   #
#       ###############################################
#
#
#
#
#   **** Os dados da empresa foram alterado para manter o sigilo    ****
#
#
import os
import time
import DB


class c_style:
    S_HEADER = '\033[31m'
    S_BLUE = '\033[94m'
    S_GREEN = '\033[92m'
    S_YELLOW = '\033[93m'
    S_RED = '\033[91m'
    S_END = '\033[0m'


mes = str(time.localtime()[1])
ano = str(time.localtime()[0])
filialGERAL = DB.filialVAREJO + DB.filialMAX

os.system("clear")
print(c_style.S_HEADER + ' ************************************************************************ \n'
                         ' ********               Gera Pedido SAP (CockPit)                ******** \n'
                         ' ********                  By_Anderson Galdino                   ******** \n'
                         ' ************************************************************************ \n' + c_style.S_END)

# solicita o numero da filial
filial = str(input(c_style.S_BLUE + 'Informe o numero da Filial:\n> '))

while filial not in filialGERAL:
    print(c_style.S_RED + 'Filial invalida...' + c_style.S_END)
    filial = str(input(c_style.S_BLUE + 'Informe o numero correto da Filial:\n> '))

if filial in DB.filialMAX:
    print(c_style.S_GREEN + "Loja: " + DB.nomeFilial[filial] + c_style.S_END)
    print(c_style.S_RED + 'Filial informada pertense ao servidor 12, rode o script no servidor 12' + c_style.S_END)
else:
    while filial != 0:
        print(c_style.S_GREEN + "Loja: " + DB.nomeFilial[filial] + c_style.S_END)
        filial = ('{:0>4}'.format(filial))
        print(c_style.S_GREEN + 'Filial: %s' % filial + c_style.S_END)
        # Defina o PDV
        pdv = int(input(c_style.S_YELLOW + 'Informe o numero do PDV:\n> '))
        pdv = ('{:0>3}'.format(pdv))
        print(c_style.S_GREEN + 'PDV: %s' % pdv + c_style.S_END)

        # Informe a data
        escolhadata = int(input(c_style.S_YELLOW + 'Data do pedido:  1 = Hoje  2 = Outro dia:\n>  '))
        while escolhadata != 1 and escolhadata != 2:
            print(c_style.S_HEADER + 'Valor invalido...' + c_style.S_END)
            escolhadata = int(input(c_style.S_YELLOW + 'Data do pedido:  1 = Hoje  2 = Outro dia:\n>  '))

        if escolhadata == 1:
            dia = int(time.localtime()[2])
            dia = ('{:0>2}'.format(dia))
            dia = str(dia)
            print(c_style.S_GREEN + 'Dia: ' + dia + c_style.S_END)

            mes = str(time.localtime()[1])
            mes = ('{:0>2}'.format(mes))
            mes = str(mes)
            print(c_style.S_GREEN + 'Mes: ' + mes + c_style.S_END)

            ano = str(time.localtime()[0])
            print(c_style.S_GREEN + 'Ano: ' + ano + c_style.S_END)

        else:
            dia = int(input(c_style.S_YELLOW + 'Informe o DIA do pedido (apenas o DIA):\n> '))
            while dia > 31 or dia < 1:
                print(c_style.S_HEADER + 'Valor invalido...' + c_style.S_END)
                dia = int(input(c_style.S_YELLOW + 'Informe o DIA do pedido (apenas o DIA):\n> '))

            dia = ('{:0>2}'.format(dia))
            print(c_style.S_GREEN + 'Dia: ' + dia + c_style.S_END)
            dia = int(dia)

            mes = int(input(c_style.S_YELLOW + 'Informe o MES do pedito (apenas o MES):\n> '))

            while mes == 2 and dia > 29:
                print(c_style.S_HEADER + 'O dia informado nao e compativel com o mes 2' + c_style.S_END)
                mes = int(input(c_style.S_YELLOW + 'Informe o MES do pedito (apenas o MES):\n> '))

            while mes > 12 or mes < 1:

                print(c_style.S_HEADER + 'Valor invalido...' + c_style.S_END)
                mes = int(input(c_style.S_YELLOW + 'Informe o MES do pedito (apenas o MES):\n> '))

                while mes == 2 and dia > 29:
                    print(c_style.S_HEADER + 'O dia informado nao e compativel com o mes 2' + c_style.S_END)
                    mes = int(input(c_style.S_YELLOW + 'Informe o MES do pedito (apenas o MES):\n> '))

            mes = ('{:0>2}'.format(mes))
            mes = str(mes)
            print(c_style.S_GREEN + 'Mes: ' + mes + c_style.S_END)

            ano = int(input(c_style.S_YELLOW + 'Informe o ANO do pedido (apenas o ANO):\n> '))
            ano = str(ano)
            print(c_style.S_GREEN + 'Ano: ' + ano + c_style.S_END)

        cupom = int(input(c_style.S_YELLOW + 'Informe o numero do cupon:\n> '))
        cupom = str(cupom)
        print(c_style.S_GREEN + cupom + c_style.S_END)

        cpfcnpj = str(input(c_style.S_YELLOW + 'Informe o CPF ou CNPJ do cliente:\n> '))
        print(c_style.S_GREEN + cpfcnpj + c_style.S_END)

        print(c_style.S_BLUE + 'GO' + c_style.S_END)
        arquivoCockpit = ('/home/arquivos/%s_%sUPD.xml' % (filial, cupom))

        linha1 = str("<?xml version='1.0' encoding='ISO-8859-1' standalone='no'?>\n")
        linha2 = str("<TRANSACTION>\n")
        linha3 = str("  <STORE>%s</STORE><POS>%s</POS><TICKET>%s</TICKET><FISCAL_DAY>%s%s%s</FISCAL_DAY>\n" % (
            filial, pdv, cupom, ano, mes, dia))
        linha4 = str("  <CODE>7</CODE>\n")
        linha5 = str("  <WHAT>1</WHAT>\n")
        linha6 = str("  <SHELL_COMMAND>php -q mfft_request_sap.php --command=envia-pedido --store=%s --pos=%s --ticket"
                     "-number=%s --ticket=%s --fiscal_date=%s-%s-%s --sap-ip=10.250.10.1:50300 "
                     "--sap-user=conecto --sap-password=Conecto@2017 --sap-client=800 --doc=%s "
                     "--timeout=30</SHELL_COMMAND>\n" % (filial, pdv, cupom, cupom, ano, mes, dia, cpfcnpj))
        linha7 = str("</TRANSACTION>\n")

        with open(arquivoCockpit, 'a') as saida:
            saida.write(str(linha1 + linha2 + linha3 + linha4 + linha5 + linha6 + linha7))

        os.system("mv /home/arquivos/%s_%sUPD.xml /var/emporium/pos/SPC" % (filial, cupom))
        os.system("tail -f /var/emporium/log/mfft_request_sap_%s.log" % filial)

        filial = 0

print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Fim do Processo              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)
