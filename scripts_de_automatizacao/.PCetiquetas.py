#!/usr/bin/python3
#
#
#       ###############################################
#       #       Configurar PC de Etiqetas Varejo      #
#       #       Versão 1.4                            #
#       #       Data 01/03/2021                       #
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
    S_GREEN = '\033[92m'
    S_YELLOW = '\033[93m'
    S_RED = '\033[91m'
    S_END = '\033[0m'


os.system("clear")
print(c_style.S_HEADER + ' ******************************************************* \n'
                         ' ********  Configurar Computador de Etiquetas   ******** \n'
                         ' ********          By_Anderson Galdino          ******** \n'
                         ' ******************************************************* \n' + c_style.S_END)

# solicita o numero da filial
filial = int(input(c_style.S_YELLOW + 'Informe o numero da Filial:\n> ' + c_style.S_END))
filial = str(filial)
while filial not in (DB.filialVAREJO or DB.filialMAX):
    print(c_style.S_RED + 'Filial invalida...')
    filial = int(input(c_style.S_YELLOW + 'Informe o numero correto da Filial:\n> ' + c_style.S_END))
    filial = str(filial)

if filial in (DB.filialVAREJO or DB.filialMAX):

    while filial != 0:
        print(c_style.S_GREEN + "Loja: " + DB.nomeFilial[filial] + c_style.S_END)
        # solicita o PDV para Transformação
        pdv = '210'

        ip = '10.%s.2.%s' % (filial, pdv)

        print(c_style.S_YELLOW + "Copiando arquivos..." + c_style.S_END)

        if filial in DB.filialMAX:
            os.system("scp -r htdocs_MAX %s:/var/www/" % ip)
            os.system("ssh %s 'mv /var/www/htdocs_MAX /var/www/htdocs/'" % ip)

        else:
            os.system("scp -r htdocs_Varejo %s:/var/www/" % ip)
            os.system("ssh %s 'mv /var/www/htdocs_Varejo /var/www/htdocs/'" % ip)

        os.system("scp php.ini %s:/etc/" % ip)
        os.system("scp httpd.conf %s:/etc/httpd/" % ip)

        print(c_style.S_GREEN + "Configurando..." + c_style.S_END)
        os.system("ssh %s 'chmod -R 777 /var/www/htdocs/'" % ip)
        os.system("ssh %s 'chmod +x /etc/rc.d/rc.httpd'" % ip)
        os.system("ssh %s 'chmod +x /etc/rc.d/rc.cups'" % ip)
        os.system("ssh %s '/etc/rc.d/rc.cups start'" % ip)
        os.system("ssh %s '/etc/rc.d/rc.httpd start'" % ip)
        os.system("ssh %s '/usr/sbin/ntpdate a.st1.ntp.br'" % ip)
        os.system("ssh %s 'init 6'" % ip)
        print(c_style.S_RED +
              "***** Inserir o IP no navegador (10.%s.2.210) para acessar o portal *****\n\n" % filial + c_style.S_END)
        print(c_style.S_GREEN +
              "***** Instalar a impressora de Etiquetas  *****\n\n"
              "Link: http://10.%s.2.210/admin.php\n"
              "Link: http://localhost/admin.php?action=login\n\n" % filial + c_style.S_END)

        filial = 0

print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Fim do Processo              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)
