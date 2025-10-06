# apps/catalog/views.py
from __future__ import annotations

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.core.mail import EmailMultiAlternatives

from .models import Vantagem
# Assumindo que Carteira e Cupom estão em apps.wallet.models
from apps.wallet.models import Cupom, Carteira # Importação adicionada para usar Carteira.debitar


# ==========================
# Helpers (e-mail)
# ==========================

def _render_primeiro_que_existir(possiveis: list[str], contexto: dict) -> str | None:
    """
    Tenta renderizar templates na ordem dada; retorna o conteúdo do primeiro que existir.
    """
    for path in possiveis:
        try:
            return render_to_string(path, contexto)
        except TemplateDoesNotExist:
            continue
    return None


def _enviar_email_resgate(user, cupom: Cupom) -> None:
    """
    Envia e-mail de confirmação de resgate.
    """
    destinatario = getattr(user, "email", None)
    if not destinatario:
        return

    # ✅ CORREÇÃO: Contexto completo para os templates .html e .txt
    ctx = {
        "aluno": user,  # Variável esperada no cupom_resgatado.txt
        "custo": cupom.vantagem.custo_moedas,  # Variável esperada no cupom_resgatado.txt
        "usuario": user,
        "vantagem": cupom.vantagem,
        "codigo": cupom.codigo,
        "empresa": cupom.vantagem.empresa,
        "data": timezone.now(),
        "cupom": cupom,
    }

    subject = f"Seu cupom: {cupom.vantagem.titulo}"
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "Moeda Acadêmica <no-reply@example.com>")
    to = [destinatario]

    # Renderização (tenta os templates mais específicos primeiro)
    html_body = _render_primeiro_que_existir(
        ["emails/cupom_resgatado.html", "emails/resgate_confirmado.html"],
        ctx,
    )
    text_body = _render_primeiro_que_existir(
        ["emails/cupom_resgatado.txt", "emails/resgate_confirmado.txt"],
        ctx,
    )

    # Fallback puro texto (se não encontrou nenhum template)
    if not html_body and not text_body:
        text_body = (
            f"Olá {user.first_name or user.username},\n\n"
            f"Você resgatou a vantagem '{cupom.vantagem.titulo}'.\n"
            f"Código: {cupom.codigo}\n"
            f"Parceiro: {cupom.vantagem.empresa.nome}\n\n"
            f"Bom proveito!"
        )

    # Envio do e-mail
    # ✅ CORREÇÃO: Passa o corpo de texto como o corpo principal, e o HTML como anexo.
    msg = EmailMultiAlternatives(subject, text_body or "", from_email, to)
    if html_body:
        msg.attach_alternative(html_body, "text/html")

    # fail_silently=False é bom para debugar, mas pode ser True em produção
    msg.send(fail_silently=False)


# ==========================
# Views
# ==========================

class VantagensListView(ListView):
    model = Vantagem
    template_name = "catalog/vantagens_list.html"
    context_object_name = "vantagens"

    def get_queryset(self):
        return (
            Vantagem.objects
            .select_related("empresa")
            .order_by("titulo")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
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


@login_required
@transaction.atomic
# ✅ CORREÇÃO PRINCIPAL: Alterado 'pk' para 'vantagem_id' para corresponder ao urls.py
def resgatar_vantagem(request: HttpRequest, vantagem_id: int) -> HttpResponse:
    """
    Resgata a vantagem (apenas ALUNO). Cria Cupom, registra extrato se possível
    e envia e-mail usando templates em templates/emails/cupom_resgatado.*.
    """
    if request.method != "POST":
        return redirect("vantagens_list")

    user = request.user
    if getattr(user, "role", "").upper() != "ALUNO":
        messages.error(request, "Apenas alunos podem resgatar vantagens.")
        return redirect("vantagens_list")

    # ✅ CORREÇÃO: Usa 'vantagem_id'
    vantagem = get_object_or_404(Vantagem.objects.select_related("empresa"), pk=vantagem_id)

    # evita resgatar repetido
    if Cupom.objects.filter(usuario=user, vantagem=vantagem).exists():
        messages.info(request, "Você já resgatou esta vantagem.")
        return redirect("vantagens_list")

    # Tenta registrar débito no extrato/saldo
    try:
        # Tenta usar o método debitar da Carteira
        carteira, _ = Carteira.objects.get_or_create(usuario=user)
        carteira.debitar(
            valor=vantagem.custo_moedas,
            descricao=f"Resgate da vantagem: {vantagem.titulo}",
            referencia=f"empresa:{vantagem.empresa.nome}",
        )
    except ValueError:
        messages.error(request, "Saldo insuficiente para resgatar esta vantagem.")
        return redirect("vantagens_list")
    except Exception:
        # Se Carteira ou Transacao não existirem ou houver outro erro, avisa e interrompe o resgate
        messages.error(request, "Erro ao processar débito. Verifique sua carteira.")
        # O transaction.atomic irá reverter o resgate se houvesse alguma escrita antes
        return redirect("vantagens_list")

    # Cria o cupom
    codigo = None
    if hasattr(Cupom, "gerar_codigo") and callable(Cupom.gerar_codigo):
        codigo = Cupom.gerar_codigo()

    cupom = Cupom.objects.create(
        usuario=user,
        vantagem=vantagem,
        codigo=codigo,
        gerado_em=timezone.now(),
    )
    
    # Envia e-mail
    if user.email:
        try:
            _enviar_email_resgate(user, cupom)
        except Exception as e:
            # Em debug, isso é útil. Em prod, deve ser logado.
            print(f"ERRO DE ENVIO DE E-MAIL: {e}")
            messages.warning(request, "Vantagem resgatada, mas houve um erro ao enviar o e-mail.")
    else:
        messages.info(request, "Vantagem resgatada, mas seu perfil não possui e-mail.")

    messages.success(request, f"Vantagem resgatada com sucesso! Seu cupom ('{cupom.codigo}') foi gerado.")
    return redirect("vantagens_list")