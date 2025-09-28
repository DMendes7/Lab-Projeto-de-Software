from django.contrib import admin
from django.utils.html import format_html
from .models import Vantagem


@admin.register(Vantagem)
class VantagemAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "custo_moedas", "ativa", "thumb")
    list_filter = ("ativa", "empresa")
    search_fields = ("titulo", "descricao", "empresa__nome")
    readonly_fields = ("preview",)
    fields = (
        "titulo",
        "descricao",
        "empresa",
        "custo_moedas",
        "ativa",
        "imagem",     # upload local
        "foto_url",   # compatibilidade com URL antiga (opcional)
        "preview",    # pré-visualização
    )

    def thumb(self, obj):
        url = obj.image_url
        if url:
            return format_html('<img src="{}" style="height:38px;border-radius:6px;" />', url)
        return "—"
    thumb.short_description = "Imagem"

    def preview(self, obj):
        url = obj.image_url
        if url:
            return format_html('<img src="{}" style="max-width:320px;border-radius:10px;" />', url)
        return "Sem imagem"
    preview.short_description = "Pré-visualização"
