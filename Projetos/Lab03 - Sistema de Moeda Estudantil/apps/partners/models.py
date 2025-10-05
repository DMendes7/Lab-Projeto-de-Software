# apps/partners/models.py
from django.conf import settings
from django.db import models
from django.db.models import Q


class EmpresaParceira(models.Model):
    """
    Empresa parceira que oferece vantagens no catálogo.
    - 'nome' é usado na listagem do catálogo e no admin.
    - 'ativa' controla se aparece no sistema.
    - 'conta' é o usuário (role=EMPRESA ou PARCEIRO) que fará login
      para ver o dashboard apenas dos resgates das vantagens desta empresa.
    """
    nome = models.CharField(max_length=120)
    cnpj = models.CharField(max_length=18, blank=True)  # opcional (00.000.000/0000-00)
    ativa = models.BooleanField(default=True)

    conta = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="empresa_parceira",
        help_text=(
            "Usuário com papel EMPRESA/PARCEIRO que acessa o dashboard desta empresa."
        ),
        # Aceita tanto EMPRESA quanto PARCEIRO para compatibilizar com os usuários existentes
        limit_choices_to=Q(role__in=["EMPRESA", "PARCEIRO"]),
    )

    class Meta:
        verbose_name = "Empresa Parceira"
        verbose_name_plural = "Empresas Parceiras"
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome
