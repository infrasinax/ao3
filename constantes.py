#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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
# Arquivo:    constantes.py                                                              #
#                                                                                        #
##########################################################################################

####    ARRAY GLOBAL POS   ####
# POS     NOME            TIPO
# 0       nome            string
# 1       login           string
# 2       senha           string
# 3       luid            int
# 4       appversion      string
# 5       ports           string
# 6       avalport        string
# 7       dbhost          string
# 8       pgdbase         string
# 9       nxpbase         string
# 10      appbase         string
# 11      mongohost       string
# 12      mongoDB         string
# 13      timezone        string
# 14      oldgen1         int
# 15      oldgen2         int
# 16      nursery         int
# 17      cpulimit        int
# 18      memlimit        int
# 19      shost           string
# 20      tamanho         int
# 21      CriaUser        int
# 22      CurForm         int
# 23      DbHostid        int
# 24      ClienteDbid     int
# 25      TipoServico     string
# 26      AppHostId       string

global globais
globais = ["","","",0,"","","","","","","","","","",0,0,0,0,0,"",0,0,0,0,0,"",0]


def TipoOS():
    import platform
    if platform.dist()[0] == "Red Hat":
        return "Red Hat"
    elif platform.dist()[0] == "CentOS":
        return "Red Hat"
    elif platform.dist()[0] == "Debian":
        return "Debian"
    elif platform.dist()[0] == "Ubuntu":
        return "Debian"
    else:
        return False

class Constantes:
    TXT_BACK_TITULO = 'Bem- vindo ao configurador AO3 BPMS'
    TXT_TITULO = 'Bem-vindo ao configurador AO3'
    TXT_INIT = 'Deseja iniciar a configuracao de um cliente para BPMS?'
    TXT_CLIENTE_QTDE = "Selecione a quantidade de usuarios do cliente"
    TXT_WRD_USER = "usuario"
    TXT_WRDS_USER = "usuarios"
    TXT_VAL_CAMPOS = "Preencha as informacoes abaixo para prosseguir"+'\n'+"Utilize as setas para se movimentar entre os campos e e TAB para acessar os botoes"
    TXT_NOME_FIELD = "O campo 'Nome do Cliente' nao deve ficar em branco"
    TXT_LOGIN_FIELD = "O campo 'Login do Cliente' nao deve ficar em branco"
    TXT_NAO = "Nao"
