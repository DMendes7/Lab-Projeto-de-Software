# apps/accounts/mixins.py
from typing import Optional
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from apps.partners.models import EmpresaParceira


class EmpresaRequiredMixin(LoginRequiredMixin):
    """
    Garante que o usuário logado é uma conta de EMPRESA (ou PARCEIRO)
    e está vinculada a uma EmpresaParceira via OneToOne (campo `conta`).
    Expõe `self.empresa` para uso na view.
    """
    empresa: Optional[EmpresaParceira] = None

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        if not user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        # Aceita EMPRESA e PARCEIRO como o mesmo papel
        role = (getattr(user, "role", "") or "").upper()
        if role not in {"EMPRESA", "PARCEIRO"}:
            messages.error(request, _("Acesso permitido apenas para contas de empresa."))
            # evitar loop com role_home
            return redirect("logout")

        # Tenta pegar o vínculo OneToOne (tratar DoesNotExist!)
        empresa = None
        try:
            empresa = user.empresa_parceira  # related_name no modelo
        except EmpresaParceira.DoesNotExist:
            empresa = None
        except AttributeError:
            empresa = None

        # Fallback defensivo
        if not isinstance(empresa, EmpresaParceira):
            empresa = EmpresaParceira.objects.filter(conta=user).first()

        if not empresa:
            messages.error(
                request,
                _(
                    "Sua conta ainda não está vinculada a uma Empresa Parceira. "
                    "Peça ao administrador para vincular sua conta à empresa."
                ),
            )
            # evitar redirecionar para role_home (causa loop); desloga e volta pro login
            return redirect("logout")

        self.empresa = empresa
        return super().dispatch(request, *args, **kwargs)
