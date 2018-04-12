#!/bin/bash
##########################################################################################
# -------------------------------------------------------------------------------------  #
#     APLICAÇÃO PARA A CRIAÇÃO DE CONTAS E CONTÊINERES DOCKER PARA CLIENTES AO3 BPMS     #
# -------------------------------------------------------------------------------------  #
# Autor:      Cristiano de Morais Lima                                                   #
# E-mail:     cristiano.lima@sinax.com.br                                                #
# Data:       11 de Abril de 2018                                                        #
# Versão:     1.0                                                                        #
# Linguagem:  Shell Script                                                               #
# Arquivo:    setup.sh                                                                   #
#                                                                                        #
##########################################################################################

if [ $UID != 0 ]; then
	sudo python config.py
	exit 1
else
	python config.py
	exit 1
fi
