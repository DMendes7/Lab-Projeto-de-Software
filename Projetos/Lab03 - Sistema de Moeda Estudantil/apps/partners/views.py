# apps/partners/views.py
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from apps.accounts.mixins import EmpresaRequiredMixin
from apps.wallet.models import Cupom
from .forms import ResgatesFilterForm


class EmpresaResgatesListView(EmpresaRequiredMixin, ListView):
    """
    Dashboard da empresa parceira.
    Lista cupons resgatados das vantagens desta empresa.
    Filtros: período (data_ini/data_fim) e vantagem.
    """
    template_name = "partners/resgates_list.html"
    context_object_name = "resgates"
    paginate_by = 50  # se quiser paginação

    def _build_form(self):
        # Passa a empresa no __init__ para o queryset da combo de vantagens
        form = ResgatesFilterForm(self.request.GET or None, empresa=self.empresa)
        # dispara validação para termos cleaned_data no template
        form.is_valid()
        return form

    def get_queryset(self):
        form = self._build_form()

        qs = (
            Cupom.objects.filter(vantagem__empresa=self.empresa)
            .select_related("usuario", "vantagem")
            .order_by("-gerado_em", "-id")
        )

        # Aplica filtros se válidos
        if form.is_valid():
            di = form.cleaned_data.get("data_ini")
            df = form.cleaned_data.get("data_fim")
            vantagem = form.cleaned_data.get("vantagem")

            if di:
                qs = qs.filter(gerado_em__date__gte=di)
            if df:
                qs = qs.filter(gerado_em__date__lte=df)
            if vantagem:
                qs = qs.filter(vantagem=vantagem)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = self._build_form()
        ctx["form"] = form
        ctx["empresa"] = self.empresa
        ctx["total"] = ctx["resgates"].count()
        return ctx


@method_decorator(require_POST, name="dispatch")
class ConsumirCupomView(EmpresaRequiredMixin, View):
    """
    Marca um cupom como consumido (apenas uma vez).
    Garante que o cupom pertence a uma vantagem da empresa logada.
    """
    def post(self, request, *args, **kwargs):
        cupom_id = kwargs.get("cupom_id")
        cupom = get_object_or_404(
            Cupom,
            id=cupom_id,
            vantagem__empresa=self.empresa,  # evita consumir cupom de outra empresa
        )

        if cupom.consumido_em:
            messages.info(request, "Este cupom já foi marcado como consumido anteriormente.")
            return redirect(self._dashboard_url())

        cupom.consumido_em = timezone.now()
        cupom.save(update_fields=["consumido_em"])

        messages.success(request, "Cupom marcado como consumido com sucesso.")
        return redirect(self._dashboard_url())

    def _dashboard_url(self):
        """
        Tenta usar o namespace/rota das empresas, com fallback para uma rota genérica se necessário.
        Ajuste o nome caso seu urls.py use outro name.
        """
        try:
            return reverse("partners:dashboard")
        except Exception:
            return reverse("dashboard_empresa")
