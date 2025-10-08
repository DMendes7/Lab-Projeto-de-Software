#!/usr/bin/env bash
set -o errexit

# use o Python do runtime do Render
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip show gunicorn || true

# coletar estáticos e aplicar migrações
python manage.py collectstatic --no-input
python manage.py migrate
