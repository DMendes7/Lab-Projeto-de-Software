# apps/partners/forms.py
from django import forms
from django.utils import timezone

from apps.catalog.models import Vantagem


class ResgatesFilterForm(forms.Form):
    """
    Filtro para o dashboard da empresa:
      - Período (data inicial/final)
      - Vantagem específica (limitada às vantagens da empresa logada)

    Use assim na view:
        form = ResgatesFilterForm(request.GET or None, empresa=self.empresa)
    """
    data_ini = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="De",
    )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Até",
    )
    vantagem = forms.ModelChoiceField(
        queryset=Vantagem.objects.none(),
        required=False,
        label="Vantagem",
    )

    def __init__(self, *args, empresa=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.empresa = empresa

        # defaults de data: últimos 30 dias
        if not self.data.get("data_ini") and not self.initial.get("data_ini"):
            self.initial["data_ini"] = timezone.localdate() - timezone.timedelta(days=30)
        if not self.data.get("data_fim") and not self.initial.get("data_fim"):
            self.initial["data_fim"] = timezone.localdate()

        # Ajusta o queryset de vantagem assim que soubermos a empresa
        if self.empresa:
            self.fields["vantagem"].queryset = (
                Vantagem.objects.filter(empresa=self.empresa, ativa=True)
                .order_by("titulo")
            )

    def clean(self):
        cleaned = super().clean()
        di = cleaned.get("data_ini")
        df = cleaned.get("data_fim")
        if di and df and di > df:
            raise forms.ValidationError("A data inicial não pode ser maior que a data final.")
        return cleaned
