from .models import Cliente
from django.db import transaction

@transaction.atomic
def criar_cliente(data: dict) -> Cliente:
    return Cliente.objects.create(**data)

@transaction.atomic
def atualizar_cliente(pk: int, data: dict) -> Cliente:
    c = Cliente.objects.get(pk=pk)
    for k, v in data.items():
        setattr(c, k, v)
    c.save()
    return c

@transaction.atomic
def excluir_cliente(pk: int) -> None:
    Cliente.objects.filter(pk=pk).delete()
