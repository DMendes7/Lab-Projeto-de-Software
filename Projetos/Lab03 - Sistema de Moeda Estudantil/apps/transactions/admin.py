from django.contrib import admin
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo", "valor", "data_hora", "descricao", "referencia")
    list_filter = ("tipo", "data_hora")
    search_fields = ("usuario__username", "descricao", "referencia")
