# apps/transactions/services.py
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.wallet.services import CarteiraService
from apps.transactions.models import Transacao

User = get_user_model()

TIPO_ENVIO = "ENVIO"
TIPO_RECEBIMENTO = "RECEBIMENTO"
TIPO_RESGATE = "RESGATE"


class TransacaoService:
    @staticmethod
    @transaction.atomic
    def registrar_envio(professor, aluno, valor, motivo):
        """
        Debita a carteira do professor e credita a do aluno, registrando as transações.
        Lança ValueError se saldo insuficiente ou valor inválido.
        """
        if valor is None or int(valor) <= 0:
            raise ValueError("O valor deve ser um inteiro positivo.")
        valor = int(valor)

        # 1) Debitar professor (histórico de ENVIO)
        CarteiraService.debitar(
            professor,
            valor,
            motivo=f"Envio ao aluno {aluno.username}: {motivo}"
        )
        Transacao.objects.create(
            usuario=professor,
            tipo=TIPO_ENVIO,
            valor=valor,
            data_hora=timezone.now(),
            descricao=motivo,
            referencia=f"para:{aluno.username}",
        )

        # 2) Creditar aluno (histórico de RECEBIMENTO)
        CarteiraService.creditar(
            aluno,
            valor,
            motivo=f"Recebido do prof. {professor.username}: {motivo}"
        )
        Transacao.objects.create(
            usuario=aluno,
            tipo=TIPO_RECEBIMENTO,
            valor=valor,
            data_hora=timezone.now(),
            descricao=motivo,
            referencia=f"de:{professor.username}",
        )

    @staticmethod
    @transaction.atomic
    def registrar_resgate(*, aluno=None, valor=None, motivo=None, referencia="", **kwargs):
        """
        Registra o resgate de uma vantagem e debita a carteira do aluno.

        Retrocompatibilidade:
        - aceita `descricao=` (equivalente a `motivo`);
        - aceita `usuario=` (equivalente a `aluno`);
        - aceita `vantagem=` (objeto opcional usado para montar `referencia` e
          uma descrição padrão caso `motivo/descricao` não seja informado).

        Parâmetros conhecidos adicionais via **kwargs são ignorados com segurança.
        """
        # Back-compat: permitir passar `usuario=` no lugar de `aluno`
        usuario = aluno or kwargs.get("usuario")
        if usuario is None:
            raise ValueError("É obrigatório informar o aluno/usuario para registrar o resgate.")

        # Back-compat: permitir `descricao=` no lugar de `motivo`
        descricao_kw = kwargs.get("descricao")
        if not motivo and descricao_kw:
            motivo = descricao_kw

        # Pode vir uma vantagem para enriquecer a descrição e referência
        vantagem = kwargs.get("vantagem")

        if valor is None or int(valor) <= 0:
            raise ValueError("O valor deve ser um inteiro positivo.")
        valor = int(valor)

        # Descrição padrão se nada vier
        if not motivo:
            if vantagem is not None:
                nome_vant = getattr(vantagem, "titulo", None) or getattr(vantagem, "nome", None) or str(vantagem)
                motivo = f"Resgate da vantagem: {nome_vant}"
            else:
                motivo = "Resgate de vantagem"

        # Referência padrão se não vier
        if not referencia:
            if vantagem is not None:
                # tenta usar id/slug se existir
                ident = getattr(vantagem, "id", None) or getattr(vantagem, "pk", None) or getattr(vantagem, "slug", None)
                referencia = f"vantagem:{ident}" if ident is not None else "vantagem"

        # Debita carteira e registra transação
        CarteiraService.debitar(usuario, valor, motivo=f"Resgate: {motivo}")

        Transacao.objects.create(
            usuario=usuario,
            tipo=TIPO_RESGATE,
            valor=valor,
            data_hora=timezone.now(),
            descricao=motivo,
            referencia=referencia or "",
        )
