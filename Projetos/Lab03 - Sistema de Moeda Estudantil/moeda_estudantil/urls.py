from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("catalogo/", include("apps.catalog.urls")),
    path("parceiros/", include("apps.partners.urls")),
    path("transacoes/", include("apps.transactions.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
