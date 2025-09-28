# apps/transactions/urls.py
from django.urls import path
from .views import EnviarMoedasView, ExtratoView

urlpatterns = [
    path("enviar/", EnviarMoedasView.as_view(), name="enviar_moedas"),
    path("extrato/", ExtratoView.as_view(), name="extrato"),
]
