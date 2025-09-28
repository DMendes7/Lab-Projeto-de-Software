# apps/catalog/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .models import Vantagem
from .services import CatalogoService
from apps.wallet.models import Cupom


class VantagensListView(LoginRequiredMixin, ListView):
    """
    Lista o catálogo para usuários logados.
    - Filtra apenas vantagens ativas de empresas ativas
    - Calcula quais vantagens o ALUNO já resgatou (cupom não consumido)
    - Exponde no contexto 'redeemed_ids' (set de ids)
    """
    model = Vantagem
    template_name = "catalog/vantagens_list.html"
    context_object_name = "vantagens"

    def get_queryset(self):
        return (
            Vantagem.objects
            .filter(ativa=True, empresa__ativa=True)
            .select_related("empresa")
            .order_by("titulo")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        role = (getattr(user, "role", "") or "").upper()
        redeemed_ids = set()
        if user.is_authenticated and role == "ALUNO":
            redeemed_ids = set(
                Cupom.objects
                .filter(
                    usuario=user,
                    vantagem__in=ctx["vantagens"],
                    consumido_em__isnull=True,
                )
                .values_list("vantagem_id", flat=True)
            )

        ctx["redeemed_ids"] = redeemed_ids
        ctx["user_role"] = role
        ctx["can_resgatar"] = (role == "ALUNO")
        return ctx


class VantagemDetailView(LoginRequiredMixin, DetailView):
    """
    Página de detalhe da vantagem.
    - Exponde 'already_redeemed' (True se aluno já tem cupom ativo dessa vantagem)
    - 'can_resgatar' True somente para ALUNO
    """
    model = Vantagem
    template_name = "catalog/vantagem_detail.html"
    context_object_name = "vantagem"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        role = (getattr(user, "role", "") or "").upper()
        vantagem = ctx["vantagem"]

        already_redeemed = False
        if user.is_authenticated and role == "ALUNO":
            already_redeemed = Cupom.objects.filter(
                usuario=user, vantagem=vantagem, consumido_em__isnull=True
            ).exists()

        ctx["user_role"] = role
        ctx["can_resgatar"] = (role == "ALUNO")
        ctx["already_redeemed"] = already_redeemed
        return ctx


@login_required
def resgatar_vantagem(request, vantagem_id):
    """
    - Só ALUNO pode resgatar
    - Impede resgatar novamente se já tiver cupom ativo (não consumido)
    - Usa a service para debitar carteira, criar transação e gerar cupom
    """
    user = request.user
    role = (getattr(user, "role", "") or "").upper()
    if role != "ALUNO":
        messages.error(request, "Apenas alunos podem resgatar vantagens.")
        return redirect("vantagens_list")

    vantagem = get_object_or_404(
        Vantagem, pk=vantagem_id, ativa=True, empresa__ativa=True
    )

    # Já possui um cupom ativo para essa vantagem?
    ja_tem = Cupom.objects.filter(
        usuario=user, vantagem=vantagem, consumido_em__isnull=True
    ).exists()
    if ja_tem:
        messages.info(request, "Você já resgatou esta vantagem.")
        return redirect("vantagens_list")

    try:
        cupom = CatalogoService.resgatar_vantagem(aluno=user, vantagem=vantagem)
    except ValueError as e:
        messages.error(request, str(e))
        return redirect("vantagens_list")

    messages.success(request, f"Vantagem resgatada! Código: {cupom.codigo}")
    return redirect("extrato")
