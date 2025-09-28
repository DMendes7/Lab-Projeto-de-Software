from typing import TYPE_CHECKING
from django.db import transaction
from django.utils import timezone

from .models import Vantagem
from apps.wallet.models import Cupom
from apps.wallet.services import CarteiraService
from apps.transactions.services import TransacaoService

# Importa o modelo User só para tipagem (evita import circular em runtime)
if TYPE_CHECKING:
    from apps.accounts.models import User


class CatalogoService:
    @staticmethod
    @transaction.atomic
    def resgatar_vantagem(aluno: "User", vantagem: Vantagem) -> Cupom:
        """
        Debita a carteira do aluno, gera cupom e registra a transação de RESGATE.
        """
        CarteiraService.debitar(aluno, vantagem.custo_moedas, motivo=f"Resgate: {vantagem.titulo}")

        cupom = Cupom.objects.create(
            usuario=aluno,
            vantagem=vantagem,
            codigo=Cupom.gerar_codigo(),
            gerado_em=timezone.now(),
        )

        TransacaoService.registrar_resgate(
            aluno=aluno,
            valor=vantagem.custo_moedas,
            descricao=f"Resgate {vantagem.titulo}",
            cupom=cupom,
        )
        return cupom
