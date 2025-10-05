# apps/wallet/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required
def extrato(request):
    # Empresas não têm extrato
    role = (getattr(request.user, "role", "") or "").upper()
    if role == "EMPRESA":
        messages.error(request, "Empresas não possuem extrato.")
        return redirect("role_home")

    # O template real do projeto fica em templates/transactions/extrato.html
    # Ele já sabe como renderizar os dados do usuário logado.
    # Se você populava 'movimentos' na versão anterior, mantenha a lógica antiga aqui.
    context = {}  # coloque aqui seus dados se houver
    return render(request, "transactions/extrato.html", context)


@login_required
def transferir(request):
    # Apenas professores podem enviar moedas
    role = (getattr(request.user, "role", "") or "").upper()
    if role != "PROFESSOR":
        messages.error(request, "Apenas professores podem enviar moedas.")
        return redirect("role_home")

    if request.method == "POST":
        # Aqui entra a sua lógica real de envio de moedas (validar form, debitar/creditar etc.)
        # Mantive só a mensagem para não quebrar enquanto você não cola sua regra antiga.
        messages.success(request, "Moedas enviadas com sucesso (placeholder).")
        return redirect("enviar_moedas")

    # IMPORTANTE: use o template que o projeto já tinha
    return render(request, "transactions/envio_moedas.html")


@login_required
def cupom_list(request):
    # Se você usa um template para cupons do aluno, mantenha aqui.
    # Deixei como está — ajuste se necessário.
    return render(request, "wallet/cupom_list.html", {"cupons": []})
