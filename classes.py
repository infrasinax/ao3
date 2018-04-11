#/usr/bin/env python
# encoding: utf-8

#importação de módulos
import os, sys, pwd
from constantes import *
from pwd import getpwnam

try:
    import psycopg2
except:
    if raw_input("Não encontrei o módulo Psycopg2. É necessário instalá-lo, prosseguir?"+'\n'+"Escreva 'sim' para instalar") == "sim":
        os.system("python -m pip install psycopg2")
    else:
        os.system('clear')
        sys.exit(1)
try:
    import pymongo
except:
    if raw_input("Não encontrei o módulo PyMongo. É necessário instalá-lo, prosseguir?"+'\n'+"Escreva 'sim' para instalar") == "sim":
        os.system("python -m pip install pymongo")
    else:
        os.system('clear')
        sys.exit(1)


#Função de criação de usuário
def createUser():
    
    Sudo=isSudo()

    if Sudo is None:
        if create_pwd():
            isFinish = os.system("sudo useradd -p '" + str(globais[2]) + "' -s "+ "/bin/bash "+ "-d "+ "/home/" + globais[1].lower() + " -m "+ " -c \""+ globais[0] +"\" " + globais[1].lower())

            if isFinish == 0:
                globais[3] = getpwnam(str(globais[1])).pw_uid
                if createFolderCargas():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    else:

        if create_pwd():
            isFinish =  os.system("useradd -p '" + str(globais[2]) + "' -s "+ "/bin/bash "+ "-d "+ "/home/" + globais[1].lower() + " -m "+ " -c \""+ globais[0] +"\" " + globais[1].lower())
            if isFinish == 0:
                globais[3] = getpwnam(str(globais[1])).pw_uid
                if createFolderCargas():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

def createFolderCargas():
    counter = 0
    Sudo=isSudo()

    if Sudo is None:
        counter += os.system("sudo mkdir /home/"+str(globais[1].lower())+"/cargas")
        counter += os.system("sudo chown "+str(globais[1].lower())+":"+str(globais[1].lower())+" /home/"+str(globais[1].lower())+"/cargas")
        if counter >= 2:
            return True
        else:
            return False
    else:
        counter += os.system("mkdir /home/"+str(globais[1].lower())+"/cargas")
        counter += os.system("chown "+str(globais[1].lower())+":"+str(globais[1].lower())+" /home/"+str(globais[1].lower())+"/cargas")
        if counter >= 2:
            return True
        else:
            return False


def isSudo():
    eSudo = os.getenv("SUDO_USER")

    if str(eSudo) == "None":
        return False
    else:
        return True


#Função para verificação da existência do usuário informado
def checkUser():
    try:
        pwd.getpwnam(globais[1].lower())
        return True
    except KeyError:
        return False


#Função de Criação de base de dados
def create_user_database():
    if check_user_database() == False:
        try:
            conn = psycopg2.connect(host='localhost',database='postgres',user='ao3_db_user',password='8EMHf4Mk')
            conn.autocommit = True
            cur = conn.cursor()
            
            cur.execute("CREATE USER "+ globais[1] +"_user WITH PASSWORD '"+ globais[2] +"';")
            cur.execute("ALTER USER "+ globais[1] +"_user LOGIN;")
            cur.execute("CREATE DATABASE "+ globais[1] +"_appserver WITH TEMPLATE template1 ENCODING 'SQL_ASCII' OWNER "+ globais[1] +"_user;")
            cur.execute("GRANT CONNECT ON DATABASE "+ globais[1] +"_appserver TO "+ globais[1] +"_user;")
            cur.execute("CREATE DATABASE "+ globais[1] +"_nxp WITH TEMPLATE template1 ENCODING 'SQL_ASCII' OWNER "+ globais[1] +"_user;")
            cur.execute("GRANT CONNECT ON DATABASE "+ globais[1] +"_nxp TO "+ globais[1] +"_user;")
            cur.execute("CREATE DATABASE "+ globais[1] +"_pgd WITH TEMPLATE template1 ENCODING 'SQL_ASCII' OWNER "+ globais[1] +"_user;")
            cur.execute("GRANT CONNECT ON DATABASE "+ globais[1] +"_pgd TO "+ globais[1] +"_user;")


            return True
        except psycopg2.Error as e:
            return ("Erro{0}").format(e)
            return False
    else:
        return False

#Verifica se o usuário tem permissão na base de dados.
def check_user_database():
    try:
        conn = psycopg2.connect(host='localhost',database='postgres',user='ao3_db_user',password='8EMHf4Mk')
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT rolname FROM pg_roles WHERE rolname='"+globais[1]+"'")
        row  = cur.fetchone()

        if row == None:
            return False
        else:
            return True
    except psycopg2.Error as f:
        return False


#Função de Manipulação do Banco de dados para controle de portas em uso do pgd
def portcontrol(sqlQuery,Insere):
    try:
        pconn = psycopg2.connect(host='10.51.1.14', database='ao3_bpms_cfg', user='ao3_user', password='48C0bIV3ho3I')
        pcur = pconn.cursor()

        #Se o parâmetro "Insere" é verdadeiro retorna o resultado da inserção.
        if Insere == True:
            pcur.execute(sqlQuery)
            pexec = pcur.fetchone()
            pconn.commit()

            if not pexec:
                raise psycopg2.Error("Não foi possível executar a query."+'\n'+"Por favor, verifique!")
            else:
                globais[24] = str(pexec[0])
                pcur.close()
                pconn.close()
                return True

        else:

            curport="SELECT servidor_id,porta_numero FROM servidores INNER JOIN portas ON servidor_id = portas.porta_servidor_id\
                    WHERE servidor_ip = '"+globais[7]+"' AND servidor_database = 'False'  ORDER BY servidor_id,porta_numero;"

            pcur.execute(curport)
            pexec=pcur.fetchall()
            
            if not pexec:
                curport="SELECT servidor_id FROM servidores  WHERE servidor_ip = '"+globais[7]+"' AND servidor_database = 'False';"
                pcur.execute(curport)
                pexec=pcur.fetchone()

                _serverid= int(str(pexec[0]))
                _nextport = int("8090")
                _result = [_serverid, _nextport]
                pcur.close()
                pconn.close()

                return _result
            else:
                
                _serverid= int(str(pexec[0][0]))
                _nextport = int(str(pexec[0][1])) + 1
                _result = [_serverid, _nextport]
                pcur.close()
                pconn.close()
                
                return _result


    except (Exception, psycopg2.DatabaseError) as error:
        print('\n'+"Não foi possível executar a query abaixo: ")
        print(sqlQuery)
        print("MOTIVO:"+str(error))
        sys.exit(1)
        return False
    finally:
        if pconn is not None:
            pconn.close()



#Função para a criação da Base MongoDB
def create_mongo_db():
    
    #importa o módulo PyMongo
    from pymongo import MongoClient
    
    #Cria o nome do banco de dados
    dbname = str(globais[1])+"_pgd_prefs"

    try:
        #Conexão ao banco de dados Mongodb
        cliente = MongoClient(str(globais[11]), 27017)

        #Criação\Conexão ao de dados
        banco = cliente[dbname]

        #Criação do usuário com acesso ao banco de dados
        banco.command("createUser", globais[1], pwd=globais[2], roles=["readWrite"])

        #Salva a coleção (tabela) dpo
        criacao = banco.prefs
        prefes = {
                "user" : "pgd_user",
                "readOnly" : "false",
                "pwd" : "086a98b3ea8d989a7dd6be7752bf2d83"}
        prefs_id = criacao.insert(prefes)

        if str(prefs_id) != "":
            # SUCESSO: Banco de dados de preferências criado com sucesso.
            return True
        else:
            # ERRO: Não foi possível criar o banco de dados de preferências
            return False
   
    except pymongo.errors.ConnectionFailure, a:
        # print("    ERRO: Não foi possível conectar ao banco de dados Mongodb especificado, verifique sua conexão"+'\n'+"    {0}").format(a)
        return False
    except pymongo.errors.DuplicateKeyError, b:
        # print("    ERRO: Foi encontrada uma duplicidade de Banco de Dados:"+'\n'+"    {0}").format(c)
        exclui_mongodb(dbname)
        return False


def exclui_mongodb(DbName):
    #importa o módulo PyMongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    from pymongo.errors import ServerSelectionTimeoutError
    try:
        #Conexão ao banco de dados Mongodb
        mongoUri = "mongodb://"+str(globais[11])+":27017/"
        cliente = MongoClient(mongoUri, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        CheckDb = cliente.database_names()

        if DbName in CheckDb:
            cliente.drop_database(DbName)
            create_mongo_db()
            return True
        else:
            return False

    except ServerSelectionTimeoutError:
        return False



# Função de teste de conexão ao Banco de dados MongoDb
#Função para a criação da Base MongoDB
def testa_mongo_db():
    #importa o módulo PyMongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    from pymongo.errors import ServerSelectionTimeoutError
    
    try:
        #Conexão ao banco de dados Mongodb
        mongoUri = "mongodb://"+str(globais[11])+":27017/"
        cliente = MongoClient(mongoUri, serverSelectionTimeoutMS=10, connectTimeoutMS=20000)
        info = cliente.server_info()
        return True
    except ServerSelectionTimeoutError:
        return False


#Função de criação Senha LastPass
def create_pwd():
    try:
        if globais[0] != "" and globais[1] != "":
            globais[2] = str(os.system("lpass generate --sync=auto --username="+globais[1]+" Shared-Servidores/CLIENTES/"+globais[0]+"/"+globais[1]+" 21"))
            return True
    except:
        return False


#Função de retorno de senha LastPass
def _ret_pwd():
    try:
        if globais[0] != "" and globais[1] != "":
            try:
                os.system("lpass login --trust -f "+"cristiano.lima@sinax.com.br")
                globais[2] = str(os.system("lpass show --password '"+globais[1]+"'"))
                return True
            except:
                return False
    except:
        return False


#Função para validação da versão Maven informada
def check_maven(versao):
    erros = 0
    host = "snx-maven-repo:8082/snx/pgd:"+versao

    if versao == "latest":
        return True
    else:
        check_ver = versao.split('.')
        #print(check_ver)
        if versao.count('.') < 3:
            erros += 4
            return "    ERRO: Formato inválido de versão. Ex.: 1.33.0.XX"
        if int(check_ver[0]) > 1:
            #   print(check_ver[0])
            erros += 1
        if int(check_ver[1]) < 33:
            #  print(check_ver[1])
            erros += 1
        if int(check_ver[2]) > 0:
            # print(check_ver[2])
            erros += 1
        if erros >= 3:
            return "    ERRO: Versão inexistente, por favor, verifique!"
            return False
        else:
            return True

#Função para validação de endereço IP ou nome do Host
def check_hostname(host):
    import socket
    if socket.gethostbyname(host) == host:
        try:
            socket.inet_aton(host)
    #SUCESSO: Endereço IP válido
            return True
        except socket.error as e:
     #ERRO: Endereço IP inválio
            return False
    else:
        try:
            socket.gethostbyname(host)
      #SUCESSO: Host válido.
            return True
        except socket.erro as f:
       #ERRO: Endereço DNS inválido.
            return False


def valida_integer(valor):
    try:
        valida = int(valor)
        return True
    except ValueError:
        return False
