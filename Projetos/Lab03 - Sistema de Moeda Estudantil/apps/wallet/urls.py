# apps/wallet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("cupons/", views.cupom_list, name="cupom_list"),
    path("extrato/", views.extrato, name="extrato"),
    path("transferir/", views.transferir, name="transferir"),
    # Alias usado em templates antigos (professor)
    path("enviar/", views.transferir, name="enviar_moedas"),
]
