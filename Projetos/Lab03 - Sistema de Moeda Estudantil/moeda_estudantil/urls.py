# moeda_estudantil/urls.py
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("catalogo/", include("apps.catalog.urls")),

    # ✅ VOLTA PARA O APP QUE JÁ FUNCIONAVA
    path("transacoes/", include("apps.transactions.urls")),

    path("empresas/", include("apps.partners.urls")),
    path("admin/", admin.site.urls),
]

# Serve arquivos de mídia em DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
