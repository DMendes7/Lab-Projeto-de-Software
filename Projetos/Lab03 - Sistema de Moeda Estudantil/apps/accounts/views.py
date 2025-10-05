# apps/accounts/views.py
from decimal import Decimal
from typing import Any

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .forms import AlunoSignupForm


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
# Papel efetivo (ajustado)
# -----------------------------
def _effective_role(user) -> str:
    """
    Determina o papel efetivo priorizando grupos, mas também
    aceitando valores do campo user.role.

    Ordem:
    1) ADMIN (superuser ou grupo 'ADMIN')
    2) PROF / PROFESSOR
    3) EMPRESA (também aceita 'PARCEIRO')
    4) ALUNO
    5) fallback: campo user.role (se existir)
    """
    if not getattr(user, "is_authenticated", False):
        return ""

    if getattr(user, "is_superuser", False):
        return "ADMIN"

    group_names = {name.upper() for name in user.groups.values_list("name", flat=True)}

    if "ADMIN" in group_names:
        return "ADMIN"
    if "PROF" in group_names or "PROFESSOR" in group_names:
        return "PROF"
    # >>> ajuste chave: tratar PARCEIRO como EMPRESA
    if "EMPRESA" in group_names or "PARCEIRO" in group_names:
        return "EMPRESA"
    if "ALUNO" in group_names:
        return "ALUNO"

    role_field = (getattr(user, "role", "") or "").upper()
    if role_field in {"EMPRESA", "PARCEIRO"}:
        return "EMPRESA"
    return role_field


class CustomLoginView(LoginView):
    """Login com redirecionamento para a home por papel (role_home)."""
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("role_home")


class CustomLogoutView(LogoutView):
    """Logout simples. O Django já cuida do básico."""
    next_page = reverse_lazy("login")


def role_home(request: HttpRequest) -> HttpResponse:
    """
    Redireciona para a página inicial conforme o papel *efetivo* do usuário.
    """
    if not request.user.is_authenticated:
        return redirect("login")

    role = _effective_role(request.user)

    if role == "ADMIN":
        try:
            return redirect("admin:index")
        except Exception:
            return redirect("/admin/")

    if role == "ALUNO":
        return redirect("dashboard_aluno")

    if role in ("PROF", "PROFESSOR"):
        return redirect("dashboard_professor")

    if role == "EMPRESA":
        # >>> vai para o dashboard de parceiro/empresa
        return redirect("partners:dashboard")

    # fallback
    try:
        return render(request, "accounts/home.html", {"role": role})
    except TemplateDoesNotExist:
        return HttpResponse(
            "<h1>Moeda Estudantil</h1>"
            "<p>Bem-vindo! Crie um template em <code>templates/accounts/home.html</code> "
            "ou acesse <a href='/transacoes/extrato/'>Extrato</a>, "
            "<a href='/catalogo/'>Catálogo</a>.</p>"
        )


class DashboardAlunoView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard_aluno.html"

    def get(self, request, *args, **kwargs):
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


# --- Cadastros --------------------------------------------------------------
def signup_aluno(request: HttpRequest) -> HttpResponse:
    """
    Cadastro real de aluno usando AlunoSignupForm.
    """
    if request.method == "POST":
        form = AlunoSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Cadastro realizado! Faça login para começar.")
            return redirect("login")
    else:
        form = AlunoSignupForm()

    return render(request, "accounts/signup_aluno.html", {"form": form})


def signup_professor(request: HttpRequest) -> HttpResponse:
    """
    (Opcional) Stub simples; ajuste se tiver um form específico.
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
