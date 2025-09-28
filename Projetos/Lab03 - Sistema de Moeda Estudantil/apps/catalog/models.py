from django.db import models


class Vantagem(models.Model):
    empresa = models.ForeignKey(
        "partners.EmpresaParceira",
        on_delete=models.CASCADE,
        related_name="vantagens",
    )
    titulo = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)

    # Mantém compatibilidade com o que já existia (URL externa, opcional)
    foto_url = models.URLField(blank=True)

    # NOVO: upload de imagem local (requer Pillow instalado)
    # Em dev será salvo em MEDIA_ROOT/vantagens/
    imagem = models.ImageField(upload_to="vantagens/", blank=True, null=True)

    custo_moedas = models.PositiveIntegerField()
    ativa = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.titulo} ({self.custo_moedas} moedas)"

    @property
    def image_url(self) -> str:
        """
        URL segura para usar no template:
        - prioriza a imagem enviada (imagem.url)
        - se não houver, usa foto_url (campo antigo)
        - senão, string vazia
        """
        try:
            if self.imagem:
                return self.imagem.url
        except Exception:
            pass
        return self.foto_url or ""
