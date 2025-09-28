# apps/accounts/views.py
from decimal import Decimal
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView


# -----------------------------
# Helpers para obter o saldo
# -----------------------------
def _safe_getattr(obj: Any, path: str, default: Any = None) -> Any:
    cur = obj
    for part in path.split("."):
        if cur is None:
            return default
        cur = getattr(cur, part, None)
    return cur if cur is not None else default


def _get_saldo(user) -> Decimal:
    """
    Descobre o saldo do usuário tentando caminhos comuns.
    Se nada for encontrado, retorna Decimal('0').
    """
    candidates = [
        "saldo",
        "balance",
        "carteira.saldo",
        "carteira.balance",
        "wallet.saldo",
        "wallet.balance",
        "aluno.carteira.saldo",
        "aluno.carteira.balance",
        "professor.carteira.saldo",
        "professor.carteira.balance",
        "profile.carteira.saldo",
        "profile.wallet.saldo",
    ]
    for path in candidates:
        value = _safe_getattr(user, path, None)
        if value is not None:
            try:
                return Decimal(value)
            except Exception:
                pass
    return Decimal("0")


# -----------------------------
# Papel efetivo (Opção A)
# -----------------------------
def _effective_role(user) -> str:
    """
    Determina o papel efetivo priorizando grupos:

    1) ADMIN (superuser ou grupo 'ADMIN')
    2) PROF / PROFESSOR
    3) EMPRESA
    4) ALUNO
    5) fallback: campo user.role (se existir)

    Retorna a sigla em UPPER.
    """
    if not getattr(user, "is_authenticated", False):
        return ""

    if getattr(user, "is_superuser", False):
        return "ADMIN"

    # nomes de grupos em upper
    group_names = {name.upper() for name in user.groups.values_list("name", flat=True)}

    if "ADMIN" in group_names:
        return "ADMIN"
    if "PROF" in group_names or "PROFESSOR" in group_names:
        return "PROF"
    if "EMPRESA" in group_names:
        return "EMPRESA"
    if "ALUNO" in group_names:
        return "ALUNO"

    # fallback: campo role do usuário, se existir
    return (getattr(user, "role", "") or "").upper()


class CustomLoginView(LoginView):
    """
    Login com redirecionamento para a home por papel (role_home).
    """
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("role_home")


class CustomLogoutView(LogoutView):
    """
    Logout simples. O Django já cuida do básico.
    """
    next_page = reverse_lazy("login")


def role_home(request: HttpRequest) -> HttpResponse:
    """
    Redireciona para a página inicial conforme o papel *efetivo* do usuário,
    inferido por grupos (Opção A).
    """
    if not request.user.is_authenticated:
        return redirect("login")

    role = _effective_role(request.user)

    if role == "ADMIN":
        # Vai para o admin do Django
        try:
            return redirect("admin:index")
        except Exception:
            return redirect("/admin/")

    if role == "ALUNO":
        return redirect("dashboard_aluno")

    if role in ("PROF", "PROFESSOR"):
        return redirect("dashboard_professor")

    if role == "EMPRESA":
        # Se não existir, cai no fallback genérico mais abaixo
        try:
            return redirect("dashboard_empresa")
        except Exception:
            pass

    # Fallback genérico: tenta renderizar um template simples
    try:
        return render(request, "accounts/home.html", {"role": role})
    except TemplateDoesNotExist:
        # Se o template não existir, responde algo funcional para não quebrar.
        return HttpResponse(
            "<h1>Moeda Estudantil</h1>"
            "<p>Bem-vindo! Crie um template em <code>templates/accounts/home.html</code> "
            "ou acesse <a href='/transacoes/extrato/'>Extrato</a>, "
            "<a href='/catalogo/'>Catálogo</a>.</p>"
        )


class DashboardAlunoView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard_aluno.html"

    def get(self, request, *args, **kwargs):
        """
        Mantém o comportamento anterior, apenas incluindo `saldo_atual`
        que é o que o template espera.
        """
        context = {"saldo_atual": _get_saldo(request.user)}
        try:
            return render(request, self.template_name, context)
        except TemplateDoesNotExist:
            return HttpResponse(
                f"<h2>Dashboard do Aluno</h2>"
                f"<p><strong>Saldo atual:</strong> {context['saldo_atual']}</p>"
                "<ul>"
                "<li><a href='/transacoes/extrato/'>Ver extrato</a></li>"
                "<li><a href='/catalogo/'>Catálogo de Vantagens</a></li>"
                "<li><a href='/transacoes/transferir/'>Transferir moedas</a></li>"
                "</ul>"
            )


class DashboardProfessorView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard_professor.html"

    def get(self, request, *args, **kwargs):
        context = {"saldo_atual": _get_saldo(request.user)}
        try:
            return render(request, self.template_name, context)
        except TemplateDoesNotExist:
            return HttpResponse(
                f"<h2>Dashboard do Professor</h2>"
                f"<p><strong>Saldo atual:</strong> {context['saldo_atual']}</p>"
                "<ul>"
                "<li><a href='/transacoes/extrato/'>Ver extrato</a></li>"
                "<li><a href='/transacoes/emitir/'>Emitir moedas</a></li>"
                "</ul>"
            )


# --- Cadastros (stubs mínimos) ---------------------------------------------
def signup_aluno(request: HttpRequest) -> HttpResponse:
    """
    Stub de cadastro de aluno para manter as URLs funcionando.
    Troque por sua view/CBV real quando desejar.
    """
    if request.method == "POST":
        messages.success(request, "Cadastro de aluno concluído (exemplo). Faça login.")
        return redirect("login")

    try:
        return render(request, "accounts/signup_aluno.html", {})
    except TemplateDoesNotExist:
        return HttpResponse(
            "<h2>Cadastro de Aluno</h2>"
            "<p>Crie o template <code>templates/accounts/signup_aluno.html</code> "
            "ou troque esta view pelo seu formulário real.</p>"
        )


def signup_professor(request: HttpRequest) -> HttpResponse:
    """
    Stub de cadastro de professor para manter as URLs funcionando.
    Troque por sua view/CBV real quando desejar.
    """
    if request.method == "POST":
        messages.success(request, "Cadastro de professor concluído (exemplo). Faça login.")
        return redirect("login")

    try:
        return render(request, "accounts/signup_professor.html", {})
    except TemplateDoesNotExist:
        return HttpResponse(
            "<h2>Cadastro de Professor</h2>"
            "<p>Crie o template <code>templates/accounts/signup_professor.html</code> "
            "ou troque esta view pelo seu formulário real.</p>"
        )
