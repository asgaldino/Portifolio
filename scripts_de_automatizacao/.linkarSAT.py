#!/usr/bin/python3
#
#       ###############################################
#       #       Autimatização para Linkar SAT         #
#       #       Versão 1.7                            #
#       #       Data 23/08/2021                       #
#       #       By_Anderson Galdino                   #
#       #       Participação: Iraú Neto               #
#       #       Revisão: Eric Teixeira                #
#       ###############################################
#
#
#
#
#   **** Os dados da empresa foram alterado para manter o sigilo    ****
#
#
import os
import subprocess
import DB


# Define estilos para o script
class c_style:
    S_HEADER = '\033[31m'
    S_BLUE = '\033[94m'
    S_GREEN = '\033[92m'
    S_RED = '\033[91m'
    S_END = '\033[0m'


os.system("clear")
print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********         Automatizacao de processo          ******** \n'
                         ' ********               Linkar PDV/SAT               ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)

# solicita o numero da filial
filial = str(input(c_style.S_BLUE + 'Informe o numero da Filial:\n> ' + c_style.S_END))

while filial not in DB.filialSP:
    print(c_style.S_RED + 'Filial invalida...' + c_style.S_END)
    filial = str(input(c_style.S_BLUE + 'Informe o numero correto da Filial:\n> ' + c_style.S_END))

while filial in DB.filialSP:
    print(c_style.S_GREEN + "Loja: " + DB.nomeFilial[filial] + c_style.S_END)
    # solicita o PDV Servidor (IBOX)
    pdvX = int(input(c_style.S_BLUE + 'Informe o PDV Servidor (IBOX):\n> ' + c_style.S_END))

    if pdvX < 100:
        pdvX = pdvX + 100
        print(c_style.S_GREEN + 'PDV: %s' % pdvX + c_style.S_END)
    else:
        print(c_style.S_GREEN + 'PDV: %s' % pdvX + c_style.S_END)

    # Defina o PDV inicial
    pdvS = int(input(c_style.S_BLUE + 'Informe o PDV Cliente (IPOS):\n> ' + c_style.S_END))
    while pdvS == pdvX:
        print(c_style.S_RED + 'PDV inválido, o PDV-Cliente deve ser diferente do PDV-Servidor...' + c_style.S_END)
        pdvS = int(input(c_style.S_BLUE + 'Informe outro PDV Cliente (IPOS):\n> ' + c_style.S_END))

    if pdvS < 100:
        pdvS = pdvS + 100
        print(c_style.S_GREEN + 'PDV: %s' % pdvS + c_style.S_END)
    else:
        print(c_style.S_GREEN + 'PDV: %s' % pdvS + c_style.S_END)
    ipX = "10.%s.2.%s" % (filial, pdvX)
    ipS = "10.%s.2.%s" % (filial, pdvS)

    # Atualizando Bibliotecas do SAT
    print(c_style.S_GREEN + 'Atualizando Bibliotecas do IBOX...' + c_style.S_END)

    os.system("ssh %s 'rm /usr/lib/libsatTANCA.so'" % ipX)
    os.system("ssh %s 'rm /var/venditor/bin/libsat_v2_0_0_1_x86.so'" % ipX)
    os.system("ssh %s 'rm /usr/lib/libsat_v2_0_0_1_x86.so'" % ipX)

    os.system("scp libsat_v3_0_0_3_x86.so %s:/var/venditor/bin/" % ipX)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/libsat_v3_0_0_3_x86.so'" % ipX)
    os.system("scp libsat_v3_0_0_3_x86.so %s:/usr/lib/" % ipX)
    os.system("ssh %s 'chmod 777 /usr/lib/libsat_v3_0_0_3_x86.so'" % ipX)
    os.system("ssh %s 'ln -s /usr/lib/libsat_v3_0_0_3_x86.so /usr/lib/libsatTANCA.so'" % ipX)

    os.system("scp libSAT.so %s:/var/venditor/bin/" % ipX)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/libSAT.so'" % ipX)
    os.system("scp libSAT.so %s:/usr/lib/" % ipX)
    os.system("ssh %s 'chmod 777 /usr/lib/libSAT.so'" % ipX)

    print(c_style.S_GREEN + 'Atualizando Bibliotecas do IPOS...' + c_style.S_END)

    os.system("ssh %s 'rm /usr/lib/libsatTANCA.so'" % ipS)
    os.system("ssh %s 'rm /var/venditor/bin/libsat_v2_0_0_1_x86.so'" % ipS)
    os.system("ssh %s 'rm /usr/lib/libsat_v2_0_0_1_x86.so'" % ipS)

    os.system("scp libsat_v3_0_0_3_x86.so %s:/var/venditor/bin/" % ipS)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/libsat_v3_0_0_3_x86.so'" % ipS)
    os.system("scp libsat_v3_0_0_3_x86.so %s:/usr/lib/" % ipS)
    os.system("ssh %s 'chmod 777 /usr/lib/libsat_v3_0_0_3_x86.so'" % ipS)
    os.system("ssh %s 'ln -s /usr/lib/libsat_v3_0_0_3_x86.so /usr/lib/libsatTANCA.so'" % ipS)

    os.system("scp libSAT.so %s:/var/venditor/bin/" % ipS)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/libSAT.so'" % ipS)
    os.system("scp libSAT.so %s:/usr/lib/" % ipS)
    os.system("ssh %s 'chmod 777 /usr/lib/libSAT.so'" % ipS)

    # Criando Diretorios
    print(c_style.S_GREEN + 'Removendo Diretorios legados...' + c_style.S_END)
    print('%s:/var/ibox/' % ipX)
    os.system("ssh %s 'rm -Rf /var/ibox/'" % ipX)

    print('%s:/var/ipos/' % ipX)
    os.system("ssh %s 'rm -Rf /var/ipos/'" % ipX)

    print('%s:/var/ibox/' % ipS)
    os.system("ssh %s 'rm -Rf /var/ibox/'" % ipS)

    print('%s:/var/ipos/' % ipS)
    os.system("ssh %s 'rm -Rf /var/ipos/'" % ipS)

    print(c_style.S_GREEN + 'Criando Diretorios...' + c_style.S_END)

    print("%s:/var/ibox/" % ipX)
    os.system("ssh %s 'mkdir /var/ibox/'" % ipX)

    print("%s:/var/ibox/PRM/" % ipX)
    os.system("ssh %s 'mkdir /var/ibox/PRM/'" % ipX)

    print("%s:/var/ibox/WRK/" % ipX)
    os.system("ssh %s 'mkdir /var/ibox/WRK/'" % ipX)

    print("%s:/var/ibox/bin/" % ipX)
    os.system("ssh %s 'mkdir /var/ibox/bin/'" % ipX)

    print("%s:/var/ibox/log/" % ipX)
    os.system("ssh %s 'mkdir /var/ibox/log/'" % ipX)

    print("%s:/var/ipos/" % ipX)
    os.system("ssh %s 'mkdir /var/ipos/'" % ipX)

    print("%s:/var/ipos/PRM/" % ipX)
    os.system("ssh %s 'mkdir /var/ipos/PRM/'" % ipX)

    print("%s:/var/ipos/WRK/" % ipX)
    os.system("ssh %s 'mkdir /var/ipos/WRK/'" % ipX)

    print("%s:/var/ipos/bin/" % ipX)
    os.system("ssh %s 'mkdir /var/ipos/bin/'" % ipX)

    print("%s:/var/ipos/log/" % ipX)
    os.system("ssh %s 'mkdir /var/ipos/log/'" % ipX)

    print("%s:/var/ipos/" % ipS)
    os.system("ssh %s 'mkdir /var/ipos/'" % ipS)

    print("%s:/var/ipos/PRM/" % ipS)
    os.system("ssh %s 'mkdir /var/ipos/PRM/'" % ipS)

    print("%s:/var/ipos/WRK/" % ipS)
    os.system("ssh %s 'mkdir /var/ipos/WRK/'" % ipS)

    print("%s:/var/ipos/bin/" % ipS)
    os.system("ssh %s 'mkdir /var/ipos/bin/'" % ipS)

    print("%s:/var/ipos/log/" % ipS)
    os.system("ssh %s 'mkdir /var/ipos/log/'" % ipS)

    # Realiza a copia dos arquivos do Servidor pros PDVs
    print(c_style.S_GREEN + 'Copiando arquivos...' + c_style.S_END)
    os.system("scp ibox %s:/var/venditor/bin/" % ipX)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/ibox'" % ipX)
    os.system("scp ibox %s:/var/ibox/bin/" % ipX)
    os.system("ssh %s 'chmod 777 /var/ibox/bin/ibox'" % ipX)
    os.system("scp ipos %s:/var/venditor/bin/" % ipX)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/ipos'" % ipX)
    os.system("scp interfast_init.sh %s:/var/venditor/bin/" % ipX)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/interfast_init.sh'" % ipX)

    os.system("scp ipos %s:/var/ipos/bin/" % ipX)
    os.system("ssh %s 'chmod 777 /var/ipos/bin/ipos'" % ipX)

    os.system("scp ibox %s:/var/venditor/bin/" % ipS)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/ibox'" % ipS)
    os.system("scp ipos %s:/var/venditor/bin/" % ipS)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/ipos'" % ipS)
    os.system("scp ipos %s:/var/ipos/bin/" % ipS)
    os.system("ssh %s 'chmod 777 /var/ipos/bin/ipos'" % ipS)
    os.system("scp interfast_init.sh %s:/var/venditor/bin/" % ipS)
    os.system("ssh %s 'chmod 777 /var/venditor/bin/interfast_init.sh'" % ipS)
    print(c_style.S_GREEN + 'Fim da copia de arquivos...' + c_style.S_END)

    # Instalação e configuração do PDV IBOX (servidor)

    print(c_style.S_GREEN + 'Instalacao e configuracao do IBOX (Servidor)...\n' + c_style.S_END)

    linhacodigo = (subprocess.getoutput("ssh %s \"sed -n '/<ACTIVATION/p' /var/venditor/PRM/SAT.xml\"" % ipX))
    codigo = linhacodigo[28:linhacodigo.index('</')]
    linhacodigo2 = (subprocess.getoutput("ssh %s \"sed -n '/<LIB/p' /var/venditor/PRM/SAT.xml\"" % ipX))
    libsat = linhacodigo2[16:linhacodigo2.index('</')]

    linha1 = str("<?xml version='1.0' standalone='no'?>\n")
    linha2 = str("<SAT_ROOT vertical_items='yes' hidden='yes'>\n")
    linha3 = str("  <USE>1</USE>\n")
    linha4 = str("  <IP></IP>\n")
    linha5 = str("  <LIB>%s</LIB>\n" % libsat)
    linha6 = str("  <TIMEOUT>60</TIMEOUT>\n")
    linha7 = str("  <IBOX_PORT>8608</IBOX_PORT>\n")
    linha8 = str("  <ACTIVATION_CODE>%s</ACTIVATION_CODE>\n" % codigo)
    linha9 = str("</SAT_ROOT>\n")

    os.system('rm /home/arquivos/scripts/SAT.xml')
    arquivoSATibox = "/home/arquivos/scripts/SAT.xml"
    with open(arquivoSATibox, 'a') as saida:
        saida.write(str(linha1 + linha2 + linha3 + linha4 + linha5 + linha6 + linha7 + linha8 + linha9))
    os.system("scp /home/arquivos/scripts/SAT.xml %s:/var/ibox/PRM/" % ipX)
    os.system("ssh %s \"sed -i '/interfast_init.sh/d' /etc/inittab\"" % ipX)
    os.system(
        "ssh %s \"sed -i '/^1:12345.*/a c7:12345:respawn:/var/venditor/bin/interfast_init.sh' /etc/inittab\"" % ipX)
    print(c_style.S_GREEN + 'inittab OK' + c_style.S_END)

    print(c_style.S_GREEN + 'Fim da instalacao do IBOX (Servidor)' + c_style.S_END)

    # Instalação e configuração do IPOS (cliente)
    print(c_style.S_GREEN + 'Instalacao e configuracao do IPOS (Cliente)...\n' + c_style.S_END)

    linha1 = str("<?xml version='1.0' standalone='no'?>\n")
    linha2 = str("<SAT_ROOT vertical_items='yes' hidden='yes'>\n")
    linha3 = str("  <USE>1</USE>\n")
    linha4 = str("  <IP></IP>\n")
    linha5 = str("  <TIMEOUT>60</TIMEOUT>\n")
    linha6 = str("  <IPOS_PORT>8607</IPOS_PORT>\n")
    linha7 = str("  <IBOX_IP>%s</IBOX_IP>\n" % ipX)
    linha8 = str("  <IBOX_PORT>8608</IBOX_PORT>\n")
    linha9 = str("</SAT_ROOT>\n")

    os.system('rm /home/arquivos/scripts/SAT.xml')
    arquivoSATipos = "/home/arquivos/scripts/SAT.xml"
    with open(arquivoSATipos, 'a') as saida:
        saida.write(str(linha1 + linha2 + linha3 + linha4 + linha5 + linha6 + linha7 + linha8 + linha9))
    os.system("scp /home/arquivos/scripts/SAT.xml %s:/var/ipos/PRM/" % ipS)
    os.system("scp /home/arquivos/scripts/.ipos_recursivo/SAT.xml %s:/var/ipos/PRM/" % ipX)
    os.system('rm /home/arquivos/scripts/SAT.xml')
    os.system("ssh %s \"sed -i '/interfast_init.sh/d' /etc/inittab\"" % ipS)
    os.system(
        "ssh %s \"sed -i '/^1:12345.*/a c7:12345:respawn:/var/venditor/bin/interfast_init.sh' /etc/inittab\"" % ipS)
    print(c_style.S_GREEN + 'inittab OK' + c_style.S_END)

    print(c_style.S_GREEN + 'Fim da instalacao do POS (Cliente)' + c_style.S_END)

    # Copia os arquivos do ibox para o ipos
    print(c_style.S_GREEN + 'Copiando arquivos do IBOX (servidor) para o IPOS (cliente)...' + c_style.S_END)

    os.system("rm /home/arquivos/scripts/SAT.xml")
    os.system("rm /home/arquivos/scripts/SAT_HASH.dat")

    os.system("scp %s:/var/venditor/PRM/SAT.xml ." % ipX)
    os.system("scp %s:/var/venditor/WRK/SAT_HASH.dat ." % ipX)

    # Edita o arquivo SAT.xml no ipos
    linhasat = (subprocess.getoutput("sed -n '/<SND_IP/p' /home/arquivos/scripts/SAT.xml"))
    if '127.0.0.1' in linhasat:
        print(c_style.S_GREEN + 'Caminho OK' + c_style.S_END)
    else:
        os.system(
            "sed -i '/^<ENVIRONMENT.*/a <SND_IP>127.0.0.1</SND_IP>' /home/arquivos/scripts/SAT.xml")
        print(c_style.S_GREEN + 'Caminho alterado' + c_style.S_END)

    linhasat2 = (subprocess.getoutput("sed -n '/<SND_PORT/p' /home/arquivos/scripts/SAT.xml"))
    if '8607' in linhasat2:
        print(c_style.S_GREEN + 'Porta OK' + c_style.S_END)
    else:
        os.system(
            "sed -i '/^<SND_IP.*/a <SND_PORT>8607</SND_PORT>' /home/arquivos/scripts/SAT.xml")
        print(c_style.S_GREEN + 'Porta alterada' + c_style.S_END)

    os.system("scp SAT.xml %s:/var/venditor/PRM/" % ipS)
    os.system("scp SAT.xml %s:/var/venditor/PRM/" % ipX)
    os.system("scp SAT_HASH.dat %s:/var/venditor/WRK/" % ipS)
    os.system("rm /home/arquivos/scripts/SAT.xml")
    os.system("rm /home/arquivos/scripts/SAT_HASH.dat")

    filial = 0
print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' **     INDISPENSAVEL reiniciar os dois computadores       ** \n'
                         ' **             Reinicie os IBOX depois o IPOS             ** \n'
                         ' ************************************************************ \n' + c_style.S_END)
