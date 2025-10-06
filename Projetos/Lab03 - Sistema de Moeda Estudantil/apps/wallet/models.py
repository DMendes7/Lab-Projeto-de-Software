# apps/wallet/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings

# ✅ Use o model Transacao já existente no app "transactions"
from apps.transactions.models import Transacao


class Carteira(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="carteira",
        on_delete=models.CASCADE,
    )
    saldo = models.IntegerField(default=0)

    def creditar(self, valor: int, descricao: str = "", referencia: str = ""):
        valor = int(valor)
        self.saldo = (self.saldo or 0) + valor
        self.save(update_fields=["saldo"])
        Transacao.objects.create(
            usuario=self.usuario,
            tipo="RECEBIMENTO",
            valor=valor,
            descricao=descricao,
            referencia=referencia,
            data_hora=timezone.now(),
        )

    def debitar(self, valor: int, descricao: str = "", referencia: str = ""):
        valor = int(valor)
        if (self.saldo or 0) < valor:
            raise ValueError("Saldo insuficiente")
        self.saldo = (self.saldo or 0) - valor
        self.save(update_fields=["saldo"])
        Transacao.objects.create(
            usuario=self.usuario,
            tipo="RESGATE",
            valor=valor,
            descricao=descricao,
            referencia=referencia,
            data_hora=timezone.now(),
        )

    def __str__(self):
        return f"Carteira({self.usuario}, saldo={self.saldo})"


class Cupom(models.Model):
    """Modelo de cupom compatível com o admin (inclui consumido_em)."""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cupons",
    )
    vantagem = models.ForeignKey("catalog.Vantagem", on_delete=models.CASCADE)
    codigo = models.CharField(max_length=20, blank=True, default="")
    gerado_em = models.DateTimeField(default=timezone.now)

    # ✅ campo esperado no admin
    consumido_em = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def gerar_codigo() -> str:
        import secrets, string
        alfabeto = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(alfabeto) for _ in range(10))

    def __str__(self):
        return f"Cupom({self.usuario}, {self.vantagem}, {self.codigo})"
