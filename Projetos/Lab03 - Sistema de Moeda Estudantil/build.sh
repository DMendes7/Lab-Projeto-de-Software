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
username = "admin"

# Se o seu User usa username, garantimos isso também
if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print("✔️ Superuser criado:", username, "/", email)
else:
    print("ℹ️ Superuser já existe (username ou email).")
EOF
