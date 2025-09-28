# apps/transactions/forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EnvioMoedasForm(forms.Form):
    aluno = forms.ModelChoiceField(
        label="Aluno",
        queryset=User.objects.none(),  # será definido no __init__
        help_text="Selecione o aluno que receberá as moedas.",
    )
    valor = forms.IntegerField(
        min_value=1,
        label="Valor (moedas)",
        help_text="Quantidade de moedas a enviar (mínimo 1).",
    )
    motivo = forms.CharField(
        label="Motivo",
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Explique o motivo do envio (isso aparece no extrato).",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apenas usuários com role=ALUNO
        self.fields["aluno"].queryset = User.objects.filter(role="ALUNO").order_by("username")

        # Rótulo amigável do select
        def label_from_instance(u):
            base = u.get_username()
            if u.email:
                return f"{base} • {u.email}"
            return base

        self.fields["aluno"].label_from_instance = label_from_instance
