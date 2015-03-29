#!/bin/bash

clear

echo "Hi, $USER! Welcome to based_ssh, please look at the readme to learn more"

python ./turbo_server.py & ngrok 5000
#ngrok 5000
