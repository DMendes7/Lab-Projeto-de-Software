from django.db import models

class EmpresaParceira(models.Model):
    nome = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField()
    ativa = models.BooleanField(default=False)  # depende de aprovação institucional

    def __str__(self):
        return f"{self.nome} ({'Ativa' if self.ativa else 'Pendente'})"
