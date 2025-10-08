#!/usr/bin/env bash
set -o errexit

# usar o Python do runtime do Render
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip show gunicorn || true

# coletar estáticos
python manage.py collectstatic --no-input

python manage.py migrate partners 0003 --no-input

python manage.py migrate partners 0004 --fake --no-input || true

python manage.py migrate --no-input
