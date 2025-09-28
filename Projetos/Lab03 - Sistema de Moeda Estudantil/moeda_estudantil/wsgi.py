import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moeda_estudantil.settings")
application = get_wsgi_application()
