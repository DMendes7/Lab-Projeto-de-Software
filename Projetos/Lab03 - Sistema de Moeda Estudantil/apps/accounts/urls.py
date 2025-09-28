# apps/accounts/urls.py
from importlib import import_module
from django.urls import path

# Importação direta do módulo para evitar erros de nomes ausentes
views = import_module("apps.accounts.views")

urlpatterns = [
    # Home / roteador por papel
    path("", views.role_home, name="role_home"),

    # Autenticação
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),

    # Dashboards por papel
    path("aluno/", views.DashboardAlunoView.as_view(), name="dashboard_aluno"),
    path("professor/", views.DashboardProfessorView.as_view(), name="dashboard_professor"),
    # Se você tiver dashboard de empresa, crie a view e descomente a linha abaixo:
    # path("empresa/", views.DashboardEmpresaView.as_view(), name="dashboard_empresa"),

    # Cadastros (mantidos para compatibilidade com seus templates/links)
    path("signup/aluno/", views.signup_aluno, name="signup_aluno"),
    path("signup/professor/", views.signup_professor, name="signup_professor"),
]
