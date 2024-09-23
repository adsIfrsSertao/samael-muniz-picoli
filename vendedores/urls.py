from django.urls import path

from vendedores import views


# Define o namespace para este conjunto de URLs
app_name = 'vendedores'

urlpatterns = [
    path('', views.VendedoresList.as_view(), name='lista_vendedores'),
    path('adicionar/', views.CriarVendedor.as_view(), name='adicionar_vendedor'),
    
    path(
        '<int:pk>/editar/', 
        views.EditarVendedor.as_view(),
        name='editar_vendedor'
    ),
    
    path(
        '<int:pk>/deletar/', 
        views.DeletarVendedor.as_view(), 
        name='deletar_vendedor'
    ),
    
    path('<int:pk>/json/', views.vendedor_json, name='vendedor_json'),
]