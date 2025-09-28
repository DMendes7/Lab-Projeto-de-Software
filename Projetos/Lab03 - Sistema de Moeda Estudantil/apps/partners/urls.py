from django.urls import path
from .views import EmpresaCreateView, ResgatesListView

urlpatterns = [
    path("nova/", EmpresaCreateView.as_view(), name="empresa_create"),
    path("resgates/", ResgatesListView.as_view(), name="resgates_list"),
]
