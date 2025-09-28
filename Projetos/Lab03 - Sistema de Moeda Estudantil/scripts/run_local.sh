#!/usr/bin/env bash
# Roda o servidor local (após migrações)
set -e
source venv/bin/activate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
