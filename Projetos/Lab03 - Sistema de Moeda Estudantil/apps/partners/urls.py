# apps/partners/urls.py
from django.urls import path
from .views import EmpresaResgatesListView, ConsumirCupomView

app_name = "partners"

urlpatterns = [
    path("dashboard/", EmpresaResgatesListView.as_view(), name="dashboard"),
    path("consumir/<int:cupom_id>/", ConsumirCupomView.as_view(), name="consumir_cupom"),
]
