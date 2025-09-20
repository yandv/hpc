#!/bin/bash

# Script para executar os testes de performance
# Instala dependências Python e executa os testes

echo "Instalando dependências Python..."
pip3 install -r requirements.txt

echo "Executando testes de performance..."
python3 test_performance.py

echo "Testes concluídos!"
