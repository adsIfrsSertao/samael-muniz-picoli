from django.urls import path

from clientes import views

# Define o namespace para este conjunto de URLs
app_name = 'clientes'

urlpatterns = [
    path('', views.ClientesList.as_view(), name='lista_cliente'),
    path('adicionar/', views.CriarCliente.as_view(), name='adicionar_cliente'),
    path(
        '<int:pk>/editar/',
        views.EditarCliente.as_view(),
        name='editar_cliente',
    ),
    path(
        '<int:pk>/deletar/',
        views.DeletarCliente.as_view(),
        name='deletar_cliente',
    ),
    path('<int:pk>/json/', views.cliente_json, name='cliente_json'),
]
