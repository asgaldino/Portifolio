#!/usr/bin/python3
#
#
# Reset automatizado dos PDVs da Rede
#
# V1.0 - Anderson Galdino
#   1.0 - Realiza um "killall" em todos os PDV's
#
#
#
#
import os

class estilo:
    vermelho = '\033[31m'
    verde = '\033[92m'
    fim = '\033[0m'
    BOLD = '\033[1m'
    azul = '\033[94m'

# Lista, onde o primeiro item é a filial e o segundo item a quantidade de PDVs da filial
# Ex.:
#    '1','10' = Filial 1, Tem 10 PDVs
#
#       **** Os dados informados são fictícios para preservar o sigilo dos dados da empresa**** 
filialquantPDV = ['1', '10', '2', '15', '3', '20']

os.system("clear")
print(estilo.vermelho + ' ************************************************************ \n'
                       ' ********      Reset automatizado dos PDVs           ******** \n'
                       ' ********      V1.0: By_Anderson Galdino             ******** \n'
                       ' ************************************************************ \n' + estilo.fim)
os.system(" ")

def killall():
    #       **** Os dados informados são fictícios para preservar o sigilo dos dados da empresa****
    ip = "200.%s.200.%s" % (filial(), pdv)
    print(estilo.azul + 'PDV: %s' % pdv)
    os.system("ssh %s 'killall -9 aplicacao_0'" % ip)
    os.system("ssh %s 'killall -9 aplicacao_1'" % ip)
    return ()

def filial():
    filial = filialquantPDV[indicefilial]
    return (int(filial))

def quantpdv():
    quantpdv = filialquantPDV[indicepdv]
    return (int(quantpdv))

# Cria as variaveis de indice para percorrer a lista "filialquantPDV" tendo como valor inicial o primeiro dado da lista
indicepdv = 1
indicefilial = 0

# Inicia o bloco de repetição para 150 repetições
for i in range(150):
    # Define o numero do primeiro PDV
    pdv = 101
    # Imprime na tela o numero da filial onde esta executando no momento
    print(estilo.verde + 'Reset da Filial:' + estilo.BOLD, filial())
    # Inicia o bloco de repetição dentro da filial percorrendo todos os PDVs obedecendo a quntidade de PDVs de cada filial
    for p in range(quantpdv()):
        # Chama a função "killall"
        killall()
        # Trata a variavel "pdv" para alterar o IP e assim executar no proximo equipamento
        pdv = pdv + 1
    # Trata as variaveis "indicepdv" e "indicefilial" para avanção no item seguinte da lista e dessa forma altera
    #  a variavel "quantpdv" e a variavel "filial"
    indicepdv = indicepdv + 2
    indicefilial = indicefilial + 2
# Imprime na tela uma mensagem final
print(estilo.vermelho + ' ************************************************************ \n'
                       ' ********               Fim do Processo              ******** \n'
                       ' ************************************************************ \n' + estilo.fim)
