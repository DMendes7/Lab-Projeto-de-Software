# apps/catalog/services.py
from __future__ import annotations

import secrets
from django.db import transaction
from django.utils import timezone

from apps.wallet.models import Cupom
from apps.transactions.services import TransacaoService
from apps.notifications.email import send_cupom_resgatado


def _gerar_codigo_unico(tamanho=10) -> str:
    """
    Gera um código único (A-Z, 0-9) e garante unicidade na tabela Cupom.
    """
    while True:
        bruto = secrets.token_hex(6).upper()  # 12 chars hex, suficiente
        codigo = bruto[:tamanho]
        if not Cupom.objects.filter(codigo=codigo).exists():
            return codigo


class CatalogoService:
    @staticmethod
    @transaction.atomic
    def resgatar_vantagem(*, aluno, vantagem):
        """
        - Verifica saldo
        - Debita/lança transação de RESGATE
        - Cria Cupom (com gerado_em)
        - Envia e-mail com o cupom
        """
        valor = int(vantagem.custo_moedas or 0)
        if valor <= 0:
            raise ValueError("Custo inválido para a vantagem.")

        # Debita/lança transação (levanta ValueError se saldo insuficiente)
        TransacaoService.registrar_resgate(
            aluno=aluno,
            valor=valor,
            motivo=f"Resgate {vantagem.titulo}",
            referencia=f"vantagem:{vantagem.id}",
        )

        # Cria cupom com código único e gerado_em preenchido
        codigo = _gerar_codigo_unico()
        cupom = Cupom.objects.create(
            usuario=aluno,
            vantagem=vantagem,
            codigo=codigo,
            gerado_em=timezone.now(),  # <— evita o NOT NULL
        )

        # Envia e-mail do cupom (falha de e-mail não cancela o resgate)
        try:
            send_cupom_resgatado(
                aluno=aluno,
                vantagem=vantagem,
                codigo=codigo,
                custo=valor,
            )
        except Exception:
            pass

        return cupom
