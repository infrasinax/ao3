#/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

##########################################################################################
# -------------------------------------------------------------------------------------  #
#     APLICAÇÃO PARA A CRIAÇÃO DE CONTAS E CONTÊINERES DOCKER PARA CLIENTES AO3 BPMS     #
# -------------------------------------------------------------------------------------  #
# Autor:      Cristiano de Morais Lima                                                   #
# E-mail:     cristiano.lima@sinax.com.br                                                #
# Data:       11 de Abril de 2018                                                        #
# Versão:     1.0                                                                        #
# Linguagem:  Python 2.0                                                                 #
# Arquivo:    crt_yml.py                                                                 #
#                                                                                        #
##########################################################################################

#importação de módulos
from constantes import *
import os, errno


#Verifica se o caminho docker existe.
def verifica_caminho():
    caminho = "/opt/docker/app/"+str(globais[1])
    if not os.path.exists(caminho):
        os.makedirs(caminho)
#        print("O caminho "+caminho+" foi criado com sucesso")
        return False
    else:

        return True

#Inicialização dos contêineres
def inicia_conteineres():
    caminho = "/opt/docker/app/"+str(globais[1])
    os.system("cd "+caminho)

    if os.system("pwd") == caminho:
        os.system("docker-compose up -d")


#Cria o arquivo docker-compose.yml
def cria_yml():
        
    # """ Caminho do arquivo de contêiner cliente """"
    ymlfile = "/opt/docker/app/"+str(globais[1])+"/docker-compose.yml"
    yml=open(ymlfile,"w")
    ymllines=["version: '2.2'\n",\
            "services:\n","  pgd:\n",\
            "    image: 'snx-maven-repo:8082/snx/pgd:"+str(globais[4])+"'\n",\
            "    ports:\n","      - '"+globais[5]+":8080'\n",\
            "    environment:\n",\
            "      - LOCAL_USER_ID="+str(globais[3])+"\n",\
            "      - SNX_DB_PGD_HOST="+str(globais[7])+"\n",\
            "      - SNX_DB_PGD_NAME="+str(globais[8])+"\n",\
            "      - SNX_DB_PGD_USER="+str(globais[1])+"\n",\
            "      - SNX_DB_PGD_PWD="+str(globais[2])+"\n",\
            "      - SNX_DB_NXP_HOST="+str(globais[7])+"\n",\
            "      - SNX_DB_NXP_NAME="+str(globais[9])+"\n",\
            "      - SNX_DB_NXP_USER="+str(globais[1])+"\n",\
            "      - SNX_DB_NXP_PWD="+str(globais[2])+"\n",\
            "      - SNX_DB_APPSERVER_HOST="+str(globais[7])+"\n",\
            "      - SNX_DB_APPSERVER_NAME="+str(globais[10])+"\n",\
            "      - SNX_DB_APPSERVER_USER="+str(globais[1])+"\n",\
            "      - SNX_DB_APPSERVER_PWD="+str(globais[2])+"\n",\
            "      - SNX_MONGODB_HOST="+str(globais[11])+"\n",\
            "      - SNX_MONGODB_DB="+str(globais[12])+"\n",\
            "      - SNX_MONGODB_USER="+str(globais[1])+"\n",\
            "      - SNX_MONGODB_PWD="+str(globais[2])+"\n",\
            "      - SNX_JAVA_XMS="+str(globais[14])+"G\n",\
            "      - SNX_JAVA_XMX="+str(globais[15])+"G\n",\
            "      - SNX_JAVA_XNS="+str(globais[16])+"M\n",\
            "      - SNX_MAX_THREADS=4\n",\
            "      - SNX_COLORING_LEVEL=0\n",\
            "      - JAVA_HOME=/opt/tools/jrockit\n",\
            "      - HOME=/home/pgd\n",\
            "      - SNX_CONN_MAX_THREADS=600\n",\
            "      - SNX_CONN_MAX_SPARE_THREADS=150\n",\
            "      - SNX_CONN_ACCEPT_COUNT=10\n",\
            "      - TZ="+str(globais[13])+"\n",\
            "    volumes:\n",\
            "      - ./work:/opt/pgd/work\n",\
            "      - ./binary:/opt/pgd/data/binary\n",\
#            "      - ./"+str(globais[1])+".jar:/opt/app/server/default/deploy/nuxeo.ear/plugins/"+str(globais[1])+".jar\n",\
            "      - ./public/snx-public.war:/opt/app/server/default/deploy/snx-public.war\n",\
            "      - /home/cargas/"+str(globais[1])+":/carga\n",\
            "    cpus: "+str(globais[17])+"\n",\
            "    mem_limit: "+str(globais[18])+"G\n",\
            "    networks:\n",\
            "      - mongodb_mongodb-net\n"]
    yml.writelines(ymllines)
    yml.close()
