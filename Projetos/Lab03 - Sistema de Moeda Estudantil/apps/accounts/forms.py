from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from apps.institutions.models import Instituicao
from .models import Aluno

User = get_user_model()

class AlunoSignupForm(UserCreationForm):
    cpf = forms.CharField(max_length=20, label="CPF")
    rg = forms.CharField(max_length=20, label="RG")
    endereco = forms.CharField(max_length=200, label="Endereço")
    curso = forms.CharField(max_length=100, label="Curso")
    instituicao = forms.ModelChoiceField(
        queryset=Instituicao.objects.all(),
        empty_label="Selecione a instituição",
        label="Instituição",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = "ALUNO"
        if commit:
            user.save()
        Aluno.objects.create(
            user=user,
            cpf=self.cleaned_data["cpf"],
            rg=self.cleaned_data["rg"],
            endereco=self.cleaned_data["endereco"],
            curso=self.cleaned_data["curso"],
            instituicao=self.cleaned_data["instituicao"],
        )
        return user
