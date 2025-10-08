#!/usr/bin/env bash
set -o errexit

# usar o Python do runtime do Render
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip show gunicorn || true

# coletar estáticos e migrar
python manage.py collectstatic --no-input
python manage.py migrate --no-input

# criar superusuário sem shell (idempotente)
python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moeda_estudantil.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

USERNAME = "admin"
EMAIL = "admin@example.com"   # pode trocar, é apenas decorativo para o admin
PASSWORD = "root"

created = False
u = User.objects.filter(username=USERNAME).first()
if not u:
    extra = {}
    # Se seu User tiver um campo 'role' com constante ADMIN, tenta preencher:
    if hasattr(User, "role") and hasattr(User, "ADMIN"):
        extra["role"] = getattr(User, "ADMIN")
    try:
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD, **extra)
        created = True
    except TypeError:
        # Caso o seu create_superuser tenha assinatura diferente (campos extras obrigatórios),
        # cria primeiro normal e depois eleva a superuser.
        u = User.objects.create(username=USERNAME, email=EMAIL, **extra)
        u.set_password(PASSWORD)
        u.is_staff = True
        u.is_superuser = True
        u.save()
        created = True

print(f"[build] superuser criado={created} username={USERNAME!r}")
PY
