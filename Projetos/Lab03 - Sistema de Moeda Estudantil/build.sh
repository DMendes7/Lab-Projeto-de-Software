#!/usr/bin/env bash
set -o errexit

echo "➜ Instalando dependências..."
pip install -r requirements.txt

echo "➜ Rodando migrations..."
python manage.py migrate --noinput

echo "➜ Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Opcional: popular o banco com dados de demo
# echo "➜ Populando dados de demo..."
# python manage.py shell < scripts/seed_demo.py
