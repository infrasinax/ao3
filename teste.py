# /usr/bin/env python
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
# Arquivo:    classes.py                                                                 #
#                                                                                        #
##########################################################################################

#importação de módulos
import os, sys, pwd
from constantes import *
from pwd import getpwnam
import psycopg2

pconn = psycopg2.connect(host='10.51.1.14', database='ao3_bpms_cfg', user='ao3_user', password='48C0bIV3ho3I')

try:
    pcur = pconn.cursor()
    curport="SELECT servidor_id,porta_numero FROM servidores INNER JOIN portas ON servidor_id = portas.porta_servidor_id\
             WHERE servidor_ip = '10.51.1.13' AND servidor_database = 'False'  ORDER BY porta_numero DESC;"
    pcur.execute(curport)
    pexec=pcur.fetchall()

    if not pexec:
        curport="SELECT servidor_id FROM servidores  WHERE servidor_ip = '10.51.1.13' AND servidor_database = 'False';"
        pcur.execute(curport)
        pexec=pcur.fetchone()
        _serverid= int(str(pexec[0]))
        _nextport = int("8090")
        _result = [_serverid, _nextport]
        pcur.close()
        pconn.close()
        print("No PEXEC\n"+_result)
    else:
        _serverid= int(str(pexec[0][0]))
        _nextport = int(str(pexec[0][1])) + 1
        _result = [_serverid, _nextport]
        pcur.close()
        pconn.close()
        print(_result)
    
except (Exception, psycopg2.DatabaseError) as error:
    print('\n'+"Não foi possível executar a query abaixo: ")
    print("MOTIVO:"+str(error))
    sys.exit(1)

finally:
    if pconn is not None:
        pconn.close()
