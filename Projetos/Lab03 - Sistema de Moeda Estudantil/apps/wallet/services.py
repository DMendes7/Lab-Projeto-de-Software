# apps/wallet/services.py
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.wallet.models import Carteira

User = get_user_model()


class CarteiraService:
    @staticmethod
    def _user_field_name():
        # ajuste para 'user' se seu modelo usar esse nome
        return "usuario"

    @staticmethod
    def _get_or_create_wallet(usuario, for_update=False):
        field = CarteiraService._user_field_name()
        filters = {field: usuario}
        qs = Carteira.objects
        if for_update:
            qs = qs.select_for_update()
        carteira, _ = qs.get_or_create(**filters, defaults={"saldo": 0})
        return carteira

    @staticmethod
    def saldo(usuario) -> int:
        carteira = CarteiraService._get_or_create_wallet(usuario)
        return int(carteira.saldo or 0)

    @staticmethod
    @transaction.atomic
    def creditar(usuario, valor, motivo: str = "") -> int:
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("O valor deve ser um inteiro positivo.")
        if valor <= 0:
            raise ValueError("O valor deve ser um inteiro positivo.")

        carteira = CarteiraService._get_or_create_wallet(usuario, for_update=True)
        carteira.saldo = int(carteira.saldo or 0) + valor
        carteira.save(update_fields=["saldo"])
        return carteira.saldo

    @staticmethod
    @transaction.atomic
    def debitar(usuario, valor, motivo: str = "") -> int:
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("O valor deve ser um inteiro positivo.")
        if valor <= 0:
            raise ValueError("O valor deve ser um inteiro positivo.")

        carteira = CarteiraService._get_or_create_wallet(usuario, for_update=True)
        saldo_atual = int(carteira.saldo or 0)

        # condição correta: bloqueia apenas quando saldo < valor
        if saldo_atual < valor:
            raise ValueError("Saldo insuficiente na carteira.")

        carteira.saldo = saldo_atual - valor
        carteira.save(update_fields=["saldo"])
        return carteira.saldo
