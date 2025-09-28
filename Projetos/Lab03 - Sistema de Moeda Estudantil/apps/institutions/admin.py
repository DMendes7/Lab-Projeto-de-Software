from django.contrib import admin
from .models import Instituicao

@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    search_fields = ("nome",)
