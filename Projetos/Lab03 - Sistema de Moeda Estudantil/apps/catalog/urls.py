# apps/catalog/urls.py
from django.urls import path
from .views import VantagensListView, VantagemDetailView, resgatar_vantagem

urlpatterns = [
    path("", VantagensListView.as_view(), name="vantagens_list"),
    # detalhe correto (singular)
    path("<int:pk>/", VantagemDetailView.as_view(), name="vantagem_detail"),
    # alias só para não quebrar se algum template ainda usar 'vantagens_detail'
    path("<int:pk>/detalhe/", VantagemDetailView.as_view(), name="vantagens_detail"),
    path("<int:vantagem_id>/resgatar/", resgatar_vantagem, name="resgatar_vantagem"),
]
