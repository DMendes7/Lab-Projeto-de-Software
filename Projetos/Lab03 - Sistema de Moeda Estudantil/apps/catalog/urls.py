# apps/catalog/urls.py
from django.urls import path
from .views import VantagensListView, VantagemDetailView, resgatar_vantagem

urlpatterns = [
    path("", VantagensListView.as_view(), name="vantagens_list"),
    path("<int:pk>/", VantagemDetailView.as_view(), name="vantagem_detail"),
    path("resgatar/<int:vantagem_id>/", resgatar_vantagem, name="resgatar_vantagem"),
]
