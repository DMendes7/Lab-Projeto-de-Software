#!/usr/bin/env bash
set -o errexit

echo "➜ Instalando dependências..."
pip install -r requirements.txt

echo "➜ Rodando migrations..."
python manage.py migrate --noinput

echo "➜ Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "➜ Conferindo superuser..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model

User = get_user_model()

email = "davimlaudares@gmail.com"
password = "root"

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password)
    print("✔️ Superuser criado:", email)
else:
    print("ℹ️ Superuser já existe:", email)
EOF
