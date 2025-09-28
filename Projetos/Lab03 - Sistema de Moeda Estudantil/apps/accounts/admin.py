from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Aluno, Professor

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Função", {"fields": ("role", "ativo")}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff", "ativo")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("user", "cpf", "curso", "instituicao")
    search_fields = ("user__username", "user__first_name", "user__last_name", "cpf")

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ("user", "cpf", "departamento", "instituicao", "saldo_semestral")
    search_fields = ("user__username", "user__first_name", "user__last_name", "cpf")
