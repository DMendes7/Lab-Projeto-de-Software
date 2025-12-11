from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

class EmpresaParceiraManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(ativa=True)

class EmpresaParceira(models.Model):
    nome = models.CharField(_("nome"), max_length=120, db_index=True)
    cnpj = models.CharField(
        _("CNPJ"),
        max_length=18,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$|^\d{14}$',
                message=_("Formato de CNPJ inválido.")
            )
        ],
        help_text=_("CNPJ no formato 00.000.000/0000-00 ou 14 dígitos.")
    )
    ativa = models.BooleanField(_("ativa"), default=True)

    conta = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="empresa_parceira",
        help_text=_("Usuário com papel EMPRESA ou PARCEIRO que acessa o dashboard."),
        limit_choices_to=Q(role__in=["EMPRESA", "PARCEIRO"]),
    )

    objects = EmpresaParceiraManager()

    class Meta:
        verbose_name = _("Empresa Parceira")
        verbose_name_plural = _("Empresas Parceiras")
        ordering = ["nome"]
        constraints = [
            models.UniqueConstraint(
                fields=["cnpj"], name="unique_cnpj", condition=~models.Q(cnpj=None)
            )
        ]

    def clean(self):
        # normalize cnpj: store only digits or None
        if self.cnpj:
            digits = re.sub(r'\D', '', self.cnpj)
            if len(digits) != 14:
                raise ValidationError({"cnpj": _("CNPJ deve ter 14 dígitos.")})
            self.cnpj = digits

    def __str__(self) -> str:
        return self.nome