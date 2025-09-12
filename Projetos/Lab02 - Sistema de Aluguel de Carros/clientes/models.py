from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=180)
    profissao = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.nome} ({self.cpf})'
