# apps/catalog/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib import messages

from .models import Vantagem
from apps.wallet.models import Cupom  # ajuste se o import for diferente

class VantagensListView(ListView):
    model = Vantagem
    template_name = "catalog/vantagens_list.html"
    context_object_name = "vantagens"

    def get_queryset(self):
        # NÃO faça: for v in qs: v.image_url = ...
        # Apenas traga os dados necessários
        return (
            Vantagem.objects
            .select_related("empresa")
            .order_by("titulo")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # ids de vantagens já resgatadas pelo aluno logado (se houver)
        redeemed_ids = set()
        user = self.request.user
        if user.is_authenticated and getattr(user, "role", "").upper() == "ALUNO":
            redeemed_ids = set(
                Cupom.objects
                .filter(usuario=user)
                .values_list("vantagem_id", flat=True)
            )
        ctx["redeemed_ids"] = redeemed_ids
        return ctx


class VantagemDetailView(DetailView):
    model = Vantagem
    template_name = "catalog/vantagem_detail.html"
    context_object_name = "vantagem"


# Caso você tenha um botão de "Resgatar" no catálogo:
def resgatar_vantagem(request, pk):
    if request.method != "POST":
        return redirect("catalogo")  # ou o nome correto da lista

    if not request.user.is_authenticated or getattr(request.user, "role", "").upper() != "ALUNO":
        messages.error(request, "Apenas alunos podem resgatar vantagens.")
        return redirect("login")

    try:
        vantagem = Vantagem.objects.get(pk=pk)
    except Vantagem.DoesNotExist:
        messages.error(request, "Vantagem não encontrada.")
        return redirect("catalogo")

    # Evita resgatar repetido
    if Cupom.objects.filter(usuario=request.user, vantagem=vantagem).exists():
        messages.info(request, "Você já resgatou esta vantagem.")
        return redirect("catalogo")

    # Aqui você pode validar saldo etc. (se já fazia antes, mantenha)
    Cupom.objects.create(
        usuario=request.user,
        vantagem=vantagem,
        codigo=Cupom.gerar_codigo() if hasattr(Cupom, "gerar_codigo") else None,
    )
    messages.success(request, "Vantagem resgatada com sucesso!")
    return redirect("catalogo")
