# apps/wallet/services.py
from django.db import transaction
from django.contrib.auth import get_user_model

from apps.wallet.models import Carteira

User = get_user_model()


class CarteiraService:
    @staticmethod
    def get_or_create(usuario):
        carteira, _ = Carteira.objects.get_or_create(usuario=usuario, defaults={"saldo": 0})
        return carteira

    @staticmethod
    @transaction.atomic
    def creditar(usuario, valor, motivo=""):
        if valor is None or int(valor) <= 0:
            raise ValueError("O valor a creditar deve ser positivo.")
        valor = int(valor)
        carteira = CarteiraService.get_or_create(usuario)
        carteira.saldo = (carteira.saldo or 0) + valor
        carteira.save(update_fields=["saldo"])
        return carteira

    @staticmethod
    @transaction.atomic
    def debitar(usuario, valor, motivo=""):
        if valor is None or int(valor) <= 0:
            raise ValueError("O valor a debitar deve ser positivo.")
        valor = int(valor)
        carteira = CarteiraService.get_or_create(usuario)
        if (carteira.saldo or 0) < valor:
            raise ValueError("Saldo insuficiente na carteira.")
        carteira.saldo = int(carteira.saldo) - valor
        carteira.save(update_fields=["saldo"])
        return carteira
