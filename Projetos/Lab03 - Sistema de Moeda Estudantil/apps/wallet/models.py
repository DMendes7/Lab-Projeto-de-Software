import secrets
from django.conf import settings
from django.db import models

class Carteira(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carteira")
    saldo = models.PositiveIntegerField(default=0)

    def creditar(self, valor: int):
        self.saldo += int(valor)
        self.save(update_fields=["saldo"])

    def debitar(self, valor: int):
        valor = int(valor)
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente na carteira.")
        self.saldo -= valor
        self.save(update_fields=["saldo"])

    def __str__(self):
        return f"Carteira de {self.usuario} (saldo={self.saldo})"


class Cupom(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cupons")
    vantagem = models.ForeignKey("catalog.Vantagem", on_delete=models.CASCADE, related_name="cupons")
    codigo = models.CharField(max_length=16, unique=True)
    gerado_em = models.DateTimeField()
    consumido_em = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def gerar_codigo() -> str:
        return secrets.token_hex(6).upper()

    def __str__(self):
        return f"{self.codigo} - {self.vantagem.titulo}"
