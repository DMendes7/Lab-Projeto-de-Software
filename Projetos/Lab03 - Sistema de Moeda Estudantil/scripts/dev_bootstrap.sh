#!/usr/bin/env bash
# Prepara ambiente de DEV (sem executar o servidor)
set -e

python3 -m venv venv
source venv/bin/activate

pip install -U pip
pip install -r requirements.txt

cp -n .env.example .env || true

echo "Ambiente preparado. Próximos passos:"
echo "1) Ajuste .env se necessário"
echo "2) python manage.py makemigrations"
echo "3) python manage.py migrate"
echo "4) python manage.py createsuperuser"
