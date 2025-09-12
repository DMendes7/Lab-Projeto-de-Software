from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'rg', 'cpf', 'endereco', 'profissao']

    def clean_cpf(self):
        cpf_raw = self.cleaned_data.get('cpf', '')
        cpf = cpf_raw.replace('.', '').replace('-', '').strip()
        if not cpf.isdigit() or len(cpf) not in (11, 14):
            raise forms.ValidationError('CPF inválido.')
        return cpf_raw
