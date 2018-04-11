#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import locale, os, sys, dialog, time, crypt, getpass, spwd, socket
from pwd import getpwnam
from classes import *
from constantes import *
from crt_yml import *
try:
    from dialog import Dialog
except:
    if raw_input("Não encontrei o módulo Dialog. É necessário instalá-lo, prosseguir?"+'\n'+"Escreva 'sim' para instalar: ") == "sim":
        if TipoOS() == "Red Hat":
            if os.system("yum install python-dialog -y") != 0:
                print("Pacote necessário não encontrado.\nPor favor, verifique.")
        else:
            if os.system("apt-get install python-dialog -y") != 0:
                print("Pacote necessário não encontrado.\nPor favor, verifique.")
    else:
        os.system('clear')
        sys.exit(1)


d = Dialog(dialog='dialog', compat='dialog', autowidgetsize=False)
d.set_background_title(Constantes.TXT_BACK_TITULO)

def InitSetup():
    if TipoOS() == "Debian" and not isSudo():
        d.infobox("O usuario atual nao tem permissao de execucao ."+'\n'+"Por favor, utilize o comando 'sudo python setup.py'",height=6, width=60)
    else:
        if d.yesno(Constantes.TXT_INIT, yes_label="Sim", no_label="Cancelar", width=40)== d.OK:
            SelectSize()

def SelectSize():
    globais[22] = 0

    code,value=d.radiolist("Selecione a quantidade de usuarios do cliente", width=60, height=16, list_height=5, \
            choices=[
                ("1"," - de 1 a 49 usuarios",1),
                ("2"," - de 1 a 99 usuarios",2),
                ("3"," - de 1 a 199 usuarios",3),
                ("4"," - acima de 200 usuarios",4)
                ],yes_label="Sim",no_label="Nao")

    if code == d.OK:

        globais[20] = int(value)

        if int(value) == 1:
            globais[14] = 3
            globais[15] = 3
            globais[16] = 512
            globais[17] = 2
            globais[18] = 5

        if int(value) == 2:
            globais[14] = 5
            globais[15] = 5
            globais[16] = 1
            globais[17] = 2
            globais[18] = 8

        if int(value) == 3:
            globais[14] = 8
            globais[15] = 8
            globais[16] = 1.2
            globais[17] = 3
            globais[18] = 12

        if int(value) == 4:
            globais[14] = 10
            globais[15] = 10
            globais[16] = 2
            globais[17] = 4
            globais[18] = 16


        ValidaCampos()

    elif code == d.ESC:
        sair()
            
    else:
        sair()
            

def ValidaCampos():
    globais[22] = 1
    
    elements = [
            ("Nome do cliente: ",1,1,globais[0],1,20,20,12),
            ("Login de usuario: ",2,1,globais[1],2,20,20,12)
            ]
    code, values = d.form("Preencha as informacoes abaixo para prosseguir."+'\n'+"Utilize as setas para se movimentar entre os campos e Tab para acessar os botoes.",elements, height=20, width=70)

    if code == d.OK:
    
        if values[0] == "":
            d.infobox("O campo 'Nome do cliente' nao deve estar em branco."+'\n'+"Por favor, verifique.",height=6, width=60)
            time.sleep(0.5)
            ValidaCampos()
        else:
            globais[0] = str(values[0])
        
        if values[1] == "":
            _txt = str("O campo 'Login do Usuario', nao deve estar em branco").encode('utf-8')
            d.infobox(_txt+'\n'+"Por favor, verifique.",height=6, width=60)
            time.sleep(0.5)
            ValidaCampos()
        else:
            globais[1] = str(values[1].encode('utf-8'))
            
            # Se o usuário existe não precisa criá-lo novamente
            if checkUser():
                
                # Se o usuário existe valida a senha
                if CheckUserFrm():
                    # Se o usuário existe e a senha é valida não precisa criá-lo novamente
                    globais[21] = 0

                else:
                    time.sleep(0.5)
                    sair()
            else:
                # Se o usuário não existe,  solicita a criação
                # globais[2] = create_pwd()
                if globais[2] == "":
                    globais[2] = "em progresso"
                    globais[21]=1
        PostgresDatabase()
    elif code == d.ESC:
        sair()

    else:
        sair()


def CheckUserFrm():
    _result = ""

    code, pwds = d.passwordbox("O usuario informado ja existe."+'\n'+"Por favor, informe a senha do usuario "+globais[1], height=10, width=45, init='')

    if code == d.OK:
        try:
            enc_pwd = spwd.getspnam(globais[1])[1]
            
            if enc_pwd in ["NP", "!", "", None]:
                _result =  "Nao ha senha para o usuario '%s'" % globais[1]
            if enc_pwd in ["LK", "*"]:
                _result =  "A conta esta bloqueada"
            if enc_pwd == "!!":
                _result =  "Senha expirada"

            if crypt.crypt(pwds, enc_pwd) == enc_pwd:
                globais[2] = str(pwds)
                globais[3] = getpwnam(str(globais[1])).pw_uid 
                return True
            else:
                _result = "Senha incorreta"
                d.infobox(_result,height=6, width=60)
                return False
            

        except KeyError as e:
            _result =  "Erro desconhecido"
            _result +=  '\n'+"O usuario '%s' nao foi encontrado" % globais[1] + '\n'+str(e)
            d.infobox(_result,height=6, width=60)
    elif code == d.ESC:
        sair()
    else:
        d.infobox(_result,height=6, width=60)
        return False


def PostgresDatabase():
    globais[22] = 2
    globais[19] = socket.gethostname()
    suggesthost = ""

    if globais[19] == "snx-apps-prod":
        suggesthost = "10.51.1.12"
        globais[25] = "Produção"
    else:
        suggesthost = "10.51.1.13"
        globais[25] = "Homologação"
        
    elements = [("Servidor: ",1,1,suggesthost,1,11,14,12)]
    code, hostval = d.form("Informe o endereco IP do servidor de banco de dados.",elements, height=10, width=40)
    
    if code == d.OK:
        if check_hostname(str(hostval[0])):
            globais[7]=str(hostval[0])
            globais[8]=globais[1]+"_pgd"
            globais[9]=globais[1]+"_nxp"
            globais[10]=globais[1]+"_appserver"
            MongoDatabase()
        else:
            d.infobox("Nao foi possivel validar o endereco do servidor informado."+'\n'+"Por favor, verifique o endereco.",height=6, width=60)
            time.sleep(0.5)
            PostgresDatabase()
    elif code == d.ESC:
        sair()
    else:
        sair()


def MongoDatabase():
    globais[22] = 3
    globais[11] = ""
    
    suggesthost = "localhost"
    elements = [("Servidor: ",1,1,suggesthost,1,11,14,12)]
    code, hostval = d.form("Informe o NOME do servidor de banco de dados Mongo.",elements, height=10, width=40)
    
    if code == d.OK:

        globais[11] = str(hostval[0])

        if testa_mongo_db():
            globais[11] = str(hostval[0])
            globais[12] = globais[1]+"_pgd_prefs"
            Lastinfo()
        else:
            d.infobox("Nao foi possivel validar o endereco do servidor informado."+'\n'+"Por favor, verifique o endereco.",height=6, width=60)
            time.sleep(0.5)
            MongoDatabase()
    elif code == d.ESC:
        sair()
    else:
        sair()

def Lastinfo():
    items = 0
    AvailablePort = portcontrol("",False)

    elements = [("Versao do Maven: ",1,1,"latest",1,24,20,20),("Porta: ",2,1,str(AvailablePort[1]),2,24,20,20),("Time Zone: ",3,1,"America\Sao_Paulo",3,24,20,20)]
   
    code, values = d.form("Preencha as informacoes abaixo para prosseguir."+'\n'+"Utilize as setas para se movimentar entre os campos e Tab para acessar os botoes.",elements, height=20, width=70)

    if code == d.OK:

        if check_maven(str(values[0])):
            globais[4] = str(values[0])
            items += 1
        else:
            d.infobox("Nao foi possivel validar a versao do Maven Repo."+'\n'+"Por favor, verifique.",height=6, width=60)
            time.sleep(0.5)
            Lastinfo()

        if str(values[1]) != "":
            try:
                int(values[1])
                globais[5] = str(int(values[1]))
                globais[23] = AvailablePort[0]
                items += 1
            except ValueError as e:
                d.infobox("Porta "+values[1]+" invalida."+'\n'+"Por favor, verifique.",height=6, width=60)
                time.sleep(0.5)
                Lastinfo()
        else:
            d.infobox("O campo 'Porta' deve ser preenchido, [default: "+AvailablePort+"]"+'\n'+"Por favor, verifique.",height=6, width=60)
            time.sleep(0.5)
            Lastinfo()

        if str(values[2]) != "":
            if check_maven(str(values[2])):
                globais[13] = str(values[2])
                items += 1
            else:
                d.infobox("Versao do Maven Repo invalida.",height=6, width=60)
                time.sleep(0.5)
                Lastinfo()
        else:
            d.infobox("O campo 'Time Zone' deve ser preenchido, [default: "+AvailablePort+"]"+'\n'+"Por favor, verifique.",height=6, width=60)
            time.sleep(0.5)
            Lastinfo()

        if items >= 3:
            Confirmacao()
    elif code == d.ESC:
        sair()
    else:
        sair()


def Confirmacao():
    elements = [("Nome: ",1,1,str(globais[0]),1,16,30,20,0x2),("Login: ",2,1,str(globais[1]),2,16,24,20,0x2),\
            ("Senha: ",3,1,str(globais[2]),3,16,24,20,0x2),("Uid: ",4,1,str(globais[3]),4,16,24,20,0x2),\
            ("Versao Maven: ",5,1,str(globais[4]),5,16,24,20,0x2),("Porta: ",6,1,str(globais[5]),6,16,24,20,0x2),\
            ("Db Server: ",7,1,str(globais[7]),7,16,24,20,0x2),("Base Pgd: ",8,1,str(globais[8]),8,16,24,20,0x2),\
            ("Base Nxp: ",9,1,str(globais[9]),9,16,24,20,0x2),("Base App: ",10,1,str(globais[10]),10,16,24,20,0x2),\
            ("Db Mongo: ",11,1,str(globais[11]),11,16,24,20,0x2),("Base Mongo: ",12,1,str(globais[12]),12,16,24,20,0x2),\
            ("Timezone: ",13,1,str(globais[13]),13,16,24,20,0x2),("Java Mem 1: ",14,1,str(globais[14])+" GB",14,16,24,20,0x2),\
            ("Java Mem 2: ",15,1,str(globais[15])+" GB",15,16,24,20,0x2),("Java Nursery: ",16,1,str(globais[16]),16,16,24,20,0x2),\
            ("CPU Limit: ",17,1,str(globais[17])+" Cores",17,16,24,20,0x2),("RAM Limit: ",18,1,str(globais[18])+" GB",18,16,24,20,0x2)]
 
    code, values = d.mixedform("Os dados abaixo estao corretos?\nDeseja prosseguir?",elements, height=40, width=50,form_height=45)

    if code == d.OK:
        Configuracao()
    elif code == d.ESC:
        sair()
    else:
        sair()

def Configuracao():
    counter = 0
    d.gauge_start(text="Aguarde a finalizacao da configuracao...",height=10,width=50,percent=0)

    if globais[1] != "" and str(globais[2]) != "": #and globais[21] == 1:
        d.gauge_update(1, "Criando usuario linux")
        
        #if createUser():
        #    d.gauge_update(10, "Usuario Linux criado")

        InsertClienteQuery = "INSERT INTO clientes (cliente_nome, cliente_servidor_id, cliente_servico) VALUES ('"+str(globais[1])+"',"+str(globais[23])+",'"+str(globais[25])+"') RETURNING cliente_id;"

        d.gauge_update(7, "Atualizado o banco de dados de controle")

        if portcontrol(InsertClienteQuery,True):
            d.gauge_update(10, "Atualizado o banco de dados de controle")

        InsertCfgQuery = "INSERT INTO configuracao (config_cliente_id,config_servidor_id,config_porta,config_local_user_id,\
                config_db_username,config_dbhost_id,config_app_version,config_db_pwd,config_pgd_dbname,config_nxp_dbname,\
                config_app_dbname,config_mongo_host,config_mongo_dbname,config_java_xmssize1,config_java_xmssize2,\
                config_java_xmssize3,config_pgd_home,config_timezone,config_volumes,config_cpus_number,config_mem_limit,\
                config_network_name)VALUES('"+globais[24]+"','"+globais[7]+"','"+globais[5]+"','"+globais[3]+"','"+globais[1]+"',\
                '"+globais[23]+"','"+globais[2]+"','"+globais[8]+"','"+globais[9]+"','"+globais[10]+"','"+globais[11]+"','"+globais[12]+"',\
                '"+globais[14]+"','"+globais[15]+"','"+globais[16]+"','/opt/docker/app/"+globais[1]+"','"+globais[13]+"',\
                '/work:/opt/pgd/work;/binary:/opt/pgd/data/binary;/"+str(globais[1])+".jar;\
                /opt/app/server/default/deploy/nuxeo.ear/plugins/"+str(globais[1])+".jar;\
                /public/snx-public.war:/opt/app/server/default/deploy/snx-public.war;\
                /home/cargas/"+str(globais[1])+":/carga','"+globais[17]+"','"+globais[18]+"','mongodb_mongodb-net');"

        if portcontrol(InsertCfgQuery,True):
            d.gauge_update(12, "Atualizado o banco de dados de controle")


        d.gauge_update(15, "Criando usuario e banco de dados Postgres")

        if create_user_database():
            d.gauge_update(25, "Criado o usuario e o banco de dados postgres")
        
        d.gauge_update(28, "Criando usuario e banco de dados de preferencias MongoDB")

        if create_mongo_db():
            d.gauge_update(50, "Criado o usuario e o banco de dados de preferencias MongoDB")

        d.gauge_update(60, "Criando as pastas do Container do cliente")

        if verifica_caminho():
            d.gauge_update(75, "Criadas as pastas do Container do cliente")

        d.gauge_update(80, "Criando o arquivo de configuracao do Container cliente")

        if cria_yml():
            d.gauge_update(90, "Criado o arquivo de configuracao do Container cliente")
        
        if portcontrol():
            d.gauge_update(95, "Gravando valores em banco de dados")

        d.gauge_update(98, "Iniciando os conteineres do cliente")

        d.gauge_update(100, "Configuracao finalizada")
        
        d.gauge_stop()
    else:
        sair()

def sair():

    if d.yesno("Deseja encerrar este aplicativo?", yes_label="Sim", no_label="Cancelar", width=40) == d.OK:
        os.system('clear')
        sys.exit(1)
    else:
        if globais[22] == 0:
            SelectSize()

        if globais[22] == 1:
            ValidaCampos()

        if globais[22] == 2:
            PostgresDatabase()

        if globais[22] == 3:
            MongoDatabase()

def main():
    locale.setlocale(locale.LC_ALL, '')
    app = InitSetup()

if __name__ == "__main__":
    main()
