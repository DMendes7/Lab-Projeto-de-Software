# apps/transactions/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from apps.transactions.forms import EnvioMoedasForm
from apps.transactions.services import TransacaoService
from apps.wallet.models import Carteira
from apps.transactions.models import Transacao

User = get_user_model()


def _eh_professor(user):
    return getattr(user, "role", "").upper() == "PROFESSOR"


@method_decorator(login_required, name="dispatch")
class EnviarMoedasView(FormView):
    template_name = "transactions/envio_moedas.html"
    form_class = EnvioMoedasForm

    def dispatch(self, request, *args, **kwargs):
        if not _eh_professor(request.user):
            messages.error(request, "Apenas professores podem enviar moedas.")
            return redirect("role_home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        professor = self.request.user
        aluno = form.cleaned_data["aluno"]
        valor = form.cleaned_data["valor"]
        motivo = form.cleaned_data["motivo"]

        try:
            TransacaoService.registrar_envio(
                professor=professor,
                aluno=aluno,
                valor=valor,
                motivo=motivo,
            )
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        messages.success(self.request, f"Envio de {valor} moedas para {aluno.username} realizado.")
        return redirect("extrato")


@method_decorator(login_required, name="dispatch")
class ExtratoView(TemplateView):
    template_name = "transactions/extrato.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        # Saldo atual
        carteira = Carteira.objects.filter(usuario=user).first()
        ctx["saldo_atual"] = carteira.saldo if carteira else 0
        # Últimas transações do usuário
        ctx["transacoes"] = (
            Transacao.objects.filter(usuario=user)
            .order_by("-data_hora", "-id")[:50]
        )
        return ctx
