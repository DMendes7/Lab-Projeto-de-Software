# moeda_estudantil/settings.py
from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================
# 🔐 Segurança / Ambiente
# ============================
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1,.onrender.com"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]

# ============================
# 🚀 Aplicativos
# ============================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # WhiteNoise helper (apenas para DEV)
    "whitenoise.runserver_nostatic",

    # Apps do domínio
    "apps.accounts",
    "apps.institutions",
    "apps.partners",
    "apps.catalog",
    "apps.wallet",
    "apps.transactions",

    # Infra/util
    "apps.notifications",
    "apps.core",
]

# ============================
# ⚙️ Middleware
# ============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve estáticos em produção
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Seu middleware customizado
    "apps.core.middleware.SimpleSecurityHeaders",
]

ROOT_URLCONF = "moeda_estudantil.urls"

# ============================
# 🧱 Templates
# ============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "moeda_estudantil.wsgi.application"
ASGI_APPLICATION = "moeda_estudantil.asgi.application"

# ============================
# 🗄 Banco de Dados
# ============================
# Render → utiliza DATABASE_URL (Postgres)
# Local → mantém SQLite automaticamente
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# ============================
# 👥 Autenticação
# ============================
AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "role_home"
LOGOUT_REDIRECT_URL = "login"

# ============================
# 🌎 Localização
# ============================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ============================
# 📁 Arquivos Estáticos
# ============================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise cuida dos arquivos compactados
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ============================
# 🖼 Arquivos de Mídia
# ============================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================
# ✉️ E-mail (Configuração flexível)
# ============================

import os

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend"  # usado localmente
)

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "moeda.academica@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = f"Moeda Acadêmica <{EMAIL_HOST_USER}>"
