# apps/transactions/views.py
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)
User = get_user_model()
MAX_TRANSACOES = 50

from apps.transactions.forms import EnvioMoedasForm
from apps.transactions.services import TransacaoService
from apps.wallet.models import Carteira
from apps.transactions.models import Transacao

class ProfessorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if getattr(request.user, "role", "").upper() != "PROFESSOR":
            messages.error(request, _("Apenas professores podem enviar moedas."))
            return redirect("role_home")
        return super().dispatch(request, *args, **kwargs)


class EnviarMoedasView(ProfessorRequiredMixin, FormView):
    template_name = "transactions/envio_moedas.html"
    form_class = EnvioMoedasForm

    def get_success_url(self):
        return reverse_lazy("extrato")

    def form_valid(self, form):
        professor = self.request.user
        aluno = form.cleaned_data["aluno"]
        valor = form.cleaned_data["valor"]
        motivo = form.cleaned_data["motivo"]

        try:
            with transaction.atomic():
                TransacaoService.registrar_envio(
                    professor=professor,
                    aluno=aluno,
                    valor=valor,
                    motivo=motivo,
                )
        except ValueError as e:
            logger.exception("Falha ao registrar envio de moedas")
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        except Exception:
            logger.exception("Erro inesperado ao registrar envio de moedas")
            messages.error(self.request, _("Ocorreu um erro ao processar a transação."))
            return self.form_invalid(form)

        messages.success(
            self.request,
            _("Envio de %(valor)s moedas para %(user)s realizado.")
            % {"valor": valor, "user": aluno.username},
        )
        return redirect(self.get_success_url())


class ExtratoView(LoginRequiredMixin, TemplateView):
    template_name = "transactions/extrato.html"

    @cached_property
    def carteira(self):
        return Carteira.objects.filter(usuario=self.request.user).first()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["saldo_atual"] = self.carteira.saldo if self.carteira else 0
        ctx["transacoes"] = (
            Transacao.objects.filter(usuario=self.request.user)
            .select_related("emissor")   # exemplo: ajuste para o nome do FK real
            .order_by("-data_hora", "-id")[:MAX_TRANSACOES]
        )
        return ctx