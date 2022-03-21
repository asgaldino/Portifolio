#!/usr/bin/python3
#
# Instalador NFCE Exclusivo para filiais de varejo
#
#
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
    S_GREEN = '\033[92m'
    S_YELLOW = '\033[93m'
    S_RED = '\033[91m'
    S_END = '\033[0m'


# Tela principal do script
os.system("clear")
print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********      Instalador de NFCE Para Varejo        ******** \n'
                         ' ********        Exclusivo para varejo               ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)

# solicita o numero da filial
filial = str(input(c_style.S_YELLOW + 'Informe o numero da Filial:\n> ' + c_style.S_END))

while filial not in DB.filialVAREJO:
    print(c_style.S_RED + 'Filial invalida...' + c_style.S_END)
    filial = str(input(c_style.S_YELLOW + 'Informe o numero correto da Filial:\n> ' + c_style.S_END))

while filial != 0:
    print(c_style.S_GREEN + "Loja: " + DB.nomeFilial[filial] + c_style.S_END)

    # solicita o PDV para Instalaão
    pdv = int(input(c_style.S_YELLOW + 'Informe o numero do PDV para instalar:\n> ' + c_style.S_END))

    if pdv < 100:
        pdv = pdv + 100
        print(c_style.S_GREEN + 'PDV: %s' % pdv)
    else:
        print(c_style.S_GREEN + 'PDV: %s' % pdv)

    ip = '10.%s.2.%s' % (filial, pdv)

    # Gera o arquivo config.php com as informacoes corretas
    configfile = "./config/config_%03d.php" % (int(filial))
    fin = open("config_sample.php")
    fout = open(configfile, "wt", 666)
    for line in fin:
        if line == str("$UF='CODIGOUF';\n"):
            fout.write(line.replace('CODIGOUF', DB.filialUF[filial]))
        elif line == str("$cnpj='CODIGOCNPJ';\n"):
            fout.write(line.replace('CODIGOCNPJ', DB.filialCNPJ[filial]))
        else:
            fout.write(line)
    fin.close()
    fout.close()
    os.system("chmod 0666 %s" % configfile)

    # Checa versao do slackware
    slackV = os.popen("ssh %s 'cat /etc/slackware-version'" % ip).read()
    slackV = slackV.replace("\n", "")
    if slackV == str("Slackware 14.0"):
        print('Slackware 14.0, instalacao em andamento...')
    elif slackV == str("Slackware 14.1"):
        print('Slackware 14.1, instalacao em andamento...')
    elif slackV == str("Slackware 14.2"):
        print('Slackware 14.2, instalacao em andamento...')
    else:
        print(c_style.S_RED + 'PDV FORA DE REDE...' + c_style.S_END)
        break

    # Checa dns
    sdnsV = os.popen("ssh %s 'cat /etc/resolv.conf'" % ip).read()
    sdnsV = sdnsV.replace("\n", "")
    if sdnsV == "search muffato.com.brnameserver 10.250.1.1nameserver 10.250.1.2":
        print('DNS correta. (search muffato.com.brnameserver 10.250.1.1nameserver 10.250.1.2)')
    else:
        print(
            c_style.S_RED + 'DNS ERRADO... Precisa ser: search muffato.com.brnameserver 10.250.1.1nameserver 10.250.1.2'
            + c_style.S_END)
        print(sdnsV)
        break

    caminho_filial = ('{:0>4}'.format(filial))
    arquivoTicket = "/var/emporium/pos/PRM/%s/TICKET.xml" % caminho_filial

    # Envia arquivos e executa acoes necessarias no PDV
    print(c_style.S_GREEN + 'Instalando binarios...' + c_style.S_END)

    os.system("ssh %s 'killall -9 venditor'" % ip)
    os.system("ssh %s 'killall -9 venditorX'" % ip)

    os.system("scp -r ./NFCe/bin/* %s:/var/venditor/bin" % ip)
    os.system("scp %s %s:/var/venditor/bin/NFCe/config/config.php" % (configfile, ip))
    print(c_style.S_GREEN + 'Fim da copia dos binarios' + c_style.S_END)
    print(c_style.S_GREEN + 'Copiando parametros...' + c_style.S_END)

    os.system("scp ./NFCe/PRM/* %s:/var/venditor/PRM" % ip)
    os.system("scp %s %s:/var/venditor/PRM/TICKET.xml" % (arquivoTicket, ip))
    print(c_style.S_GREEN + 'Fim da copia de parametros' + c_style.S_END)

    # Define o tipo de impressora que sera usada
    arquivoTicket = "TICKET_EPSON.xml"
    printer = int(input(c_style.S_YELLOW + 'Qual o modelo da impressora (1=Epson, 2=Sweda, 3=Bematech,4=Elgin,'
                                           ' 5=Epson_Posto, 6=Elgin_Posto):\n> ' + c_style.S_END))

    if printer == 1:
        arquivoTicket = "TICKET_EPSON.xml"

    elif printer == 2:
        arquivoTicket = "TICKET_SWEDA.xml"

    elif printer == 3:
        arquivoTicket = "TICKET_BEMA.xml"

    elif printer == 4:
        arquivoTicket = "TICKET_ELGIN.xml"

    elif printer == 5:
        arquivoTicket = "TICKET_EPSON_POSTO.xml"

    elif printer == 6:
        arquivoTicket = "TICKET_ELGIN_POSTO.xml"

    os.system("scp ./NFCe/PRM_TICKET/%s %s:/var/venditor/PRM/TICKET.xml" % (arquivoTicket, ip))

    print(c_style.S_GREEN + 'Copiando pacotes adicionais...' + c_style.S_END)
    os.system("scp ./NFCe/udev/*.rules %s:/etc/udev/rules.d/" % ip)
    os.system("ssh %s 'mkdir -p /var/venditor/NFCE_BAD/ /var/venditor/NFCE_CONT/'" % ip)
    os.system("scp ./NFCe/usr/lib/lib* %s:/usr/lib/" % ip)
    os.system("ssh %s 'udevadm trigger' " % ip)
    # Ajusta link do php
    print(c_style.S_GREEN + 'Fim da copia dos pacotes adicionais...' + c_style.S_END)
    print(c_style.S_GREEN + 'Aplicando links...' + c_style.S_END)
    os.system("ssh %s 'if [ ! -h /var/venditor/bin/php ]; then echo alterando php; rm /var/venditor/bin/php;"
              " ln -sf /usr/bin/php /var/venditor/bin/php; /var/venditor/bin/php --version; fi'" % ip)

    # Finalizando processos que podem variar de acordo com a versao do Slackware ou modelo da impressora.
    if slackV == str("Slackware 14.0"):
        print(c_style.S_GREEN + 'Copiando e gerando libs...' + c_style.S_END)
        os.system("scp ./NFCe/usr/lib/14.0/lib* %s:/usr/lib/" % ip)
        print(c_style.S_GREEN + 'Fim da copia das libs' + c_style.S_END)
        # Atualiza libcurl
        print(c_style.S_GREEN + 'Atualizando libcurl...' + c_style.S_END)
        os.system("ssh %s 'cd /usr/lib; ln -s libcurl.so.4.3.0 libcurl.so;'" % ip)
        # Altera o Kernel
        if filial != str("72"):
            print(c_style.S_GREEN + 'Alterando kernel para SMP...' + c_style.S_END)
            os.system("ssh %s 'cd /boot; ln -sf vmlinuz-huge-smp-3.2.29-smp vmlinuz;"
                      " ln -sf config-huge-smp-3.2.29-smp config;"
                      " ln -sf System.map-huge-smp-3.2.29-smp System.map; lilo'" % ip)
            print("OK")
    elif slackV == str("Slackware 14.2"):
        # Atualiza libcurl
        print(c_style.S_GREEN + 'Atualizando libcurl...' + c_style.S_END)
        os.system("ssh %s 'cd /usr/lib; ln -s libcurl.so.4.4.0 libcurl.so.2;'" % ip)
        os.system("ssh %s 'cd /usr/lib; ln -s libcurl.so.4.4.0 libcurl.so.3;'" % ip)

    # libera driver usb
    print(c_style.S_GREEN + 'Ativando modulo usblp...' + c_style.S_END)
    os.system("ssh %s \"sed -i '16 a /sbin/modprobe usblp' /etc/rc.d/rc.modules.local\"" % ip)

    # Desabilita o apache
    print(c_style.S_GREEN + 'Desativando servicos desnecessarios...' + c_style.S_END)
    os.system("ssh %s 'chmod a-x /etc/rc.d/rc.httpd'" % ip)

    # Remove as pastas php e nfce do bin
    if DB.filialUF[filial] == str("SP"):
        print(c_style.S_GREEN + 'Removendo pastas e arquivos desnecessarios...' + c_style.S_END)
        os.system("ssh %s 'rm -r /var/venditor/bin/NFCe/'" % ip)
        os.system("ssh %s 'rm -r /var/venditor/bin/php'" % ip)
    else:
        print(c_style.S_GREEN + 'Nao ha pastas para remover!' + c_style.S_END)

    # Reinicia a maquina
    print(c_style.S_GREEN + 'Virando o PDV' + c_style.S_END)
    os.system("ssh %s 'cp /var/venditor/bin/venditor /var/venditor/WRK/'" % ip)

    print(c_style.S_GREEN + 'Fim da copia do processo' + c_style.S_END)

    filial = 0

print(c_style.S_HEADER + '******************************************************** \n'
                         '******                      Fim                   ****** \n'
                         '******************************************************** \n' + c_style.S_END)
