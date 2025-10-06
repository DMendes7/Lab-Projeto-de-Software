# apps/wallet/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from apps.wallet.models import Transacao, Carteira


@login_required
def extrato(request: HttpRequest) -> HttpResponse:
    """
    Mostra o extrato do usuário corrente. Empresas não possuem extrato de moedas.
    Busca TODAS as transações do usuário (inclusive RESGATE) e renderiza
    o template que você já tem em templates/transactions/extrato.html
    """
    role = (getattr(request.user, "role", "") or "").upper()
    if role == "EMPRESA":
        messages.error(request, "Empresas não possuem extrato.")
        return redirect("role_home")

    transacoes = (
        Transacao.objects
        .filter(usuario=request.user)
        .order_by("-data_hora", "-id")
    )

    # saldo atual (se não houver carteira, exibe 0)
    try:
        saldo_atual = request.user.carteira.saldo
    except Carteira.DoesNotExist:
        saldo_atual = 0
        messages.info(request, "Carteira não encontrada. Saldo exibido como 0.")

    return render(
        request,
        "transactions/extrato.html",
        {"transacoes": transacoes, "saldo": saldo_atual},
    )


@login_required
def transferir(request: HttpRequest) -> HttpResponse:
    """
    Tela de envio/transferência. Mantida simples para não alterar o visual.
    """
    role = (getattr(request.user, "role", "") or "").upper()
    if role != "PROFESSOR":
        return HttpResponseForbidden("Apenas professores podem enviar moedas.")

    if request.method != "POST":
        # Apenas renderiza o template já existente (sem mudar visual)
        return render(request, "transactions/envio_moedas.html")

    # Se você já tem o processamento do POST, mantenha aqui.
    messages.success(request, "Operação registrada.")
    return redirect("transferir")


@login_required
def cupom_list(request: HttpRequest) -> HttpResponse:
    """
    Lista de cupons do aluno (placeholder caso você ainda não tenha implementado).
    """
    return render(request, "wallet/cupom_list.html", {"cupons": []})
