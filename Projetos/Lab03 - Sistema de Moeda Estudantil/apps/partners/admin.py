from django.contrib import admin
from .models import EmpresaParceira

@admin.register(EmpresaParceira)
class EmpresaParceiraAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "email", "ativa")
    list_filter = ("ativa",)
    search_fields = ("nome", "cnpj")
