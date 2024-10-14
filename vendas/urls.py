from django.urls import path

from vendas import views

# Define o namespace para este conjunto de URLs
app_name = 'vendas'

urlpatterns = [
    path('', views.VendaList.as_view(), name='lista_vendas'),
    path('<int:pk>/', views.detalhe_venda, name='detalhe_venda'),
    path('adicionar/', views.CriarVenda.as_view(), name='adicionar_venda'),
    path('<int:pk>/editar/', views.EditarVenda.as_view(), name='editar_venda'),
    path(
        '<int:pk>/deletar/', views.DeletarVenda.as_view(), name='deletar_venda'
    ),
    path('<int:pk>/json/', views.venda_json, name='venda_json'),
    path('importar/', views.upload_vendas, name='importar_excel'),
    path('download/', views.download_vendas, name='download_vendas'),
    path('<int:pk>/detalhes/', views.detalhe_venda, name='detalhe_venda'),
]
