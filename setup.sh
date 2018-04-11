#!/bin/bash
if [ $UID != 0 ]; then
	sudo python config.py
	exit 1
fi
