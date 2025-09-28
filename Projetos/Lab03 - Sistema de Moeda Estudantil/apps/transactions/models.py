from django.conf import settings
from django.db import models

class TipoTransacao(models.TextChoices):
    ENVIO = "ENVIO", "Envio (débito do professor)"
    RECEBIMENTO = "RECEBIMENTO", "Recebimento (crédito do aluno)"
    RESGATE = "RESGATE", "Resgate de vantagem (débito do aluno)"

class Transacao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transacoes")
    tipo = models.CharField(max_length=15, choices=TipoTransacao.choices)
    valor = models.PositiveIntegerField()
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=255, blank=True)
    referencia = models.CharField(max_length=64, blank=True)

    # relações auxiliares p/ rastreio
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name="envios_realizados")
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="recebimentos_relacionados")
    cupom = models.ForeignKey("wallet.Cupom", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-data_hora"]

    def __str__(self):
        return f"{self.usuario} {self.tipo} {self.valor}"
