from django.contrib import admin
from .models import Carteira, Cupom

@admin.register(Carteira)
class CarteiraAdmin(admin.ModelAdmin):
    list_display = ("usuario", "saldo")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name")

@admin.register(Cupom)
class CupomAdmin(admin.ModelAdmin):
    list_display = ("codigo", "usuario", "vantagem", "gerado_em", "consumido_em")
    list_filter = ("vantagem",)
    search_fields = ("codigo", "usuario__username")
