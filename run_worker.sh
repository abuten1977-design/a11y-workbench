#!/bin/bash
# Запуск worker з venv

cd /home/butenhome/aiwork

# Активувати venv
source venv/bin/activate

# Запустити worker
python3 worker.py
