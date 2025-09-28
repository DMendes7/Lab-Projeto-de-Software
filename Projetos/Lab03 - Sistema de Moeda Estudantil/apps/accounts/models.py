from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ALUNO = "ALUNO", "Aluno"
        PROFESSOR = "PROFESSOR", "Professor"
        PARCEIRO = "PARCEIRO", "Empresa Parceira"
        STAFF = "STAFF", "Equipe/Instituição"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ALUNO)
    ativo = models.BooleanField(default=True)

    # dica: RELACIONAMENTOS
    # - Carteira (OneToOne) está no app wallet.Carteira para evitar import circular
    # - Perfis Aluno/Professor abaixo, com OneToOne para User

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


class Aluno(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="aluno")
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    curso = models.CharField(max_length=120)
    instituicao = models.ForeignKey("institutions.Instituicao", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="alunos")

    def __str__(self):
        return f"Aluno {self.user.get_full_name()}"


class Professor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="professor")
    cpf = models.CharField(max_length=14, unique=True)
    departamento = models.CharField(max_length=120)
    instituicao = models.ForeignKey("institutions.Instituicao", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="professores")
    # saldo semestral disponível para envio de moedas (além de possuir Carteira)
    saldo_semestral = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return f"Professor {self.user.get_full_name()}"
