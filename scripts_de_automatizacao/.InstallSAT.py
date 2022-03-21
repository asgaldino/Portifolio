#!/usr/bin/python3
#
#       ###############################################
#       #       Autimatização para Instalar SAT       #
#       #       Versão 2.0                            #
#       #       Data 12/01/2021                       #
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


# Define estilos para o script
class c_style:
    S_HEADER = '\033[31m'
    S_BLUE = '\033[94m'
    S_GREEN = '\033[92m'
    S_YELLOW = '\033[93m'
    S_RED = '\033[91m'
    S_END = '\033[0m'


os.system("clear")
print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********         Automatizacao de processo          ******** \n'
                         ' ********          Instalar/Deslinkar SAT            ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)

# solicita o numero da filial
filial = str(input(c_style.S_BLUE + 'Informe o numero da Filial:\n> '))
libSAT = " "
while filial not in DB.filialSP:
    print(c_style.S_RED + 'Filial invalida...' + c_style.S_END)
    filial = str(input(c_style.S_BLUE + 'Informe o numero correto da Filial:\n> '))

if filial in DB.filialSP:
    print(c_style.S_GREEN + "Loja: " + DB.nomeFilial[filial] + c_style.S_END)
    # Defina o PDV
    pdv = int(input(c_style.S_BLUE + 'Informe o PDV:\n> '))

    if pdv < 100:
        pdv = pdv + 100
        pdv = str(pdv)
        print(c_style.S_GREEN + 'PDV: %s' % pdv)
    else:
        pdv = str(pdv)
        print(c_style.S_GREEN + 'PDV: %s' % pdv + c_style.S_END)

    ip = "10.%s.2.%s" % (filial, pdv)

    codigoNovo = str(input(c_style.S_BLUE + 'Informe o Novo Codigo de Ativacao:\n> '))

    marcaSAT = str(input(c_style.S_BLUE + 'Qual a Marca do SAT?\n  1-TANCA   2-SWEDA  \n> '))
    while marcaSAT != '1' and marcaSAT != '2':
        print(c_style.S_RED + 'Opcao invalida...' + c_style.S_END)
        marcaSAT = str(input(c_style.S_BLUE + 'Informe o numero correto da opcao:\n> '))

    print(c_style.S_YELLOW + 'Copiando Lib...' + c_style.S_END)

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

    print(c_style.S_YELLOW + 'Editando SAT.xml...' + c_style.S_END)

    if marcaSAT == '1':
        libSAT = 'libsatTANCA.so'
    elif marcaSAT == '2':
        libSAT = 'libSAT.so'

    linha1 = str("<?xml version='1.0' standalone='no'?>\n")
    linha2 = str("<SAT_ROOT vertical_items='yes' hidden='yes'>\n")
    linha3 = str("&conecto_lang;\n")
    linha4 = str("&entity_yes_no_options;\n")
    linha5 = str("&entity_no_yes_options;\n")
    linha6 = str("<USE>1</USE>\n")
    linha7 = str("<DIR width='60'>../SAT</DIR>\n")
    linha8 = str("<LIB width='60'>/usr/lib/%s</LIB>\n" % libSAT)
    linha9 = str("<CNPJ width='20'>05113966000159</CNPJ>\n")
    linha10 = str("<ACTIVATION_CODE width='60'>%s</ACTIVATION_CODE>\n" % codigoNovo)
    linha11 = str("<TIMEOUT>60</TIMEOUT>\n")
    linha12 = str("<ENVIRONMENT>1</ENVIRONMENT>\n")
    linha13 = str("<SIGN_COMMAND>php -q signsat.php</SIGN_COMMAND>\n")
    linha14 = str("<STATUS_INTERVAL>10800</STATUS_INTERVAL>\n")
    linha15 = str("</SAT_ROOT>\n")

    os.system('rm SAT.xml')
    arquivoSAT = "SAT.xml"

    with open(arquivoSAT, 'a') as saida:
        saida.write(str(linha1 + linha2 + linha3 + linha4 + linha5 + linha6 + linha7 + linha8 + linha9 + linha10
                        + linha11 + linha12 + linha13 + linha14 + linha15))

    os.system("scp SAT.xml %s:/var/venditor/PRM/" % ip)

    print(c_style.S_YELLOW + 'Editando inittab...' + c_style.S_END)
    os.system("ssh %s sed -i '/interfast_init/d' /etc/inittab" % ip)

    print(c_style.S_BLUE + 'Removendo arquivos...' + c_style.S_END)
    os.system("ssh %s 'rm -Rf /var/ipos/'" % ip)
    os.system("ssh %s 'rm -Rf /var/ibox/'" % ip)
    os.system('rm SAT.xml')

    print(c_style.S_YELLOW + 'Copiando arquivos...' + c_style.S_END)
    os.system("scp certificado.pem %s:/var/venditor/bin/" % ip)
    os.system("scp signsat.php %s:/var/venditor/bin/" % ip)

    print(c_style.S_BLUE + 'Alterando permissao...' + c_style.S_END)
    os.system("ssh %s 'chmod +x /var/venditor/bin/certificado.pem'" % ip)
    os.system("ssh %s 'chmod +x /var/venditor/bin/signsat.php'" % ip)

    os.system("ssh %s 'pkill interfast_init.sh'" % ip)
    os.system("ssh %s 'pkill venditor'" % ip)
    os.system("ssh %s 'pkill venditorX'" % ip)

    print(
        c_style.S_RED + "No PDV entrar com o comando 194 > Funcao > Opcao 3\n"
                        "*****Deve retonar > SAT assinado com sucesso.*****\n\n\n\n" + c_style.S_END)

print(c_style.S_HEADER + ' ************************************************************ \n'
                         ' ********               Fim do Processo              ******** \n'
                         ' ********              By_Anderson Galdino           ******** \n'
                         ' ************************************************************ \n' + c_style.S_END)
