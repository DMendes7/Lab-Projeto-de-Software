# moeda_estudantil/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # WhiteNoise helper (opcional, útil no runserver)
    "whitenoise.runserver_nostatic",

    # Nossos apps (domínio)
    "apps.accounts",
    "apps.institutions",
    "apps.partners",
    "apps.catalog",
    "apps.wallet",
    "apps.transactions",

    # util/infra
    "apps.notifications",
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # estáticos quando DEBUG=False
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.SimpleSecurityHeaders",  # nosso middleware
]

ROOT_URLCONF = "moeda_estudantil.urls"

TEMPLATES = [{
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
}]

WSGI_APPLICATION = "moeda_estudantil.wsgi.application"
ASGI_APPLICATION = "moeda_estudantil.asgi.application"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

AUTH_USER_MODEL = "accounts.User"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "role_home"
LOGOUT_REDIRECT_URL = "login"

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Armazenamento
STORAGES = {
    "default": {  # necessário para ImageField/FileField (uploads)
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {  # WhiteNoise
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ✉️ E-mail: usar SMTP do Gmail SEMPRE (inclusive em DEBUG)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = "moeda.academica@gmail.com"
EMAIL_HOST_PASSWORD = "lhge bjpf xfyy pehe"  # 16 caracteres gerados pelo Google
DEFAULT_FROM_EMAIL = "Moeda Acadêmica <moeda.academica@gmail.com>"