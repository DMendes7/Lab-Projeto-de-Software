from django.urls import path
from .views import ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView

app_name = 'clientes'
urlpatterns = [
    path('', ClienteListView.as_view(), name='lista'),
    path('novo/', ClienteCreateView.as_view(), name='novo'),
    path('<int:pk>/editar/', ClienteUpdateView.as_view(), name='editar'),
    path('<int:pk>/excluir/', ClienteDeleteView.as_view(), name='excluir'),
]
