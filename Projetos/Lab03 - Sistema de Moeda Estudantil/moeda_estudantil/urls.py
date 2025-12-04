# moeda_estudantil/urls.py
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("catalogo/", include("apps.catalog.urls")),
    path("transacoes/", include("apps.transactions.urls")),
    path("empresas/", include("apps.partners.urls")),
    path("admin/", admin.site.urls),
]

# ======================================================
# 📸 Servir arquivos de mídia (Render + Ambiente local)
# ======================================================
# Como suas imagens são públicas (vantagens), podemos servir SEM depender de DEBUG
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
