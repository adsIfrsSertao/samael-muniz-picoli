from django.urls import path

from produtos import views

# Define o namespace para este conjunto de URLs
app_name = 'produtos'

urlpatterns = [
    path('', views.ProdutoList.as_view(), name='lista_produtos'),
    path('<int:pk>/', views.detalhe_produto, name='detalhe_produto'),
    path('adicionar/', views.CriarProduto.as_view(), name='adicionar_produto'),
    path(
        '<int:pk>/editar/',
        views.EditarProduto.as_view(),
        name='editar_produto',
    ),
    path(
        '<int:pk>/deletar/',
        views.DeletarProduto.as_view(),
        name='deletar_produto',
    ),
    path('<int:pk>/json/', views.produto_json, name='produto_json'),
]
