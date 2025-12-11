# apps/partners/admin.py
from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from apps.partners.models import EmpresaParceira
from apps.accounts.models import User  # seu user custom

ROLES_EMPRESA_VALIDOS = ["EMPRESA", "PARCEIRO"]


class EmpresaParceiraAdminForm(forms.ModelForm):
    class Meta:
        model = EmpresaParceira
        fields = ["nome", "cnpj", "ativa", "conta"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Para evitar “não é uma escolha válida” com popup/autocomplete,
        # abrimos o queryset para TODOS os usuários.
        # A regra de papel será garantida no save_model.
        self.fields["conta"].queryset = User.objects.all().order_by("username")
        self.fields["conta"].help_text = _(
            "Usuário que acessará o dashboard desta empresa. "
            "Se não for PARCEIRO/EMPRESA, ao salvar será ajustado automaticamente para PARCEIRO."
        )


@admin.register(EmpresaParceira)
class EmpresaParceiraAdmin(admin.ModelAdmin):
    """
    Admin da empresa parceira.
    - E-mail da conta vinculada.
    - Aceita criação via popup/autocomplete sem invalidar a seleção.
    - No salvar, garante role adequado.
    """
    form = EmpresaParceiraAdminForm

    list_display = ("nome", "ativa", "email", "conta")
    list_filter = ("ativa",)
    search_fields = ("nome", "conta__email", "conta__username", "cnpj")
    autocomplete_fields = ("conta",)
    fields = ("nome", "cnpj", "ativa", "conta")
    raw_id_fields = ("conta",)

    def email(self, obj):
        if obj.conta and getattr(obj.conta, "email", None):
            return obj.conta.email or "—"
        return "—"
    email.short_description = "E-mail"
    email.admin_order_field = "conta__email"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Garante papel válido para login do parceiro
        if obj.conta_id:
            user = obj.conta
            role = (getattr(user, "role", "") or "").upper()
            if role not in ROLES_EMPRESA_VALIDOS:
                user.role = "PARCEIRO"  # ajuste aqui se quiser "EMPRESA"
                user.save(update_fields=["role"])
