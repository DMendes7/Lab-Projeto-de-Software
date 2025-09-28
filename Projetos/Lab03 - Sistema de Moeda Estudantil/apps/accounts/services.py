from dataclasses import dataclass
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest

@dataclass
class AuthResult:
    ok: bool
    message: str = ""

class AuthService:
    @staticmethod
    def do_login(request: HttpRequest, username: str, password: str) -> AuthResult:
        user = authenticate(request, username=username, password=password)
        if not user:
            return AuthResult(False, "Credenciais inválidas.")
        if not getattr(user, "ativo", True):
            return AuthResult(False, "Usuário inativo.")
        login(request, user)
        return AuthResult(True)

    @staticmethod
    def do_logout(request: HttpRequest) -> None:
        logout(request)
