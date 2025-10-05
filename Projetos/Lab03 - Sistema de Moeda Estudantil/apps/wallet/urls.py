# apps/wallet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Extrato e envio (nomes antigos preservados)
    path("extrato/", views.extrato, name="extrato"),

    # Nome histórico usado no dashboard/professor e no base.html antigo
    path("enviar/", views.transferir, name="enviar_moedas"),

    # Alias opcional (pode manter se estiver usando em algum lugar novo)
    path("transferir/", views.transferir, name="transferir"),

    # Lista de cupons (se existir)
    path("cupons/", views.cupom_list, name="cupom_list"),
]
