from django.urls import path

from core import views


# Define o namespace para este conjunto de URLs
app_name = 'core'

# Lista de padrões de URL (rotas) mapeados para suas respectivas views
urlpatterns = [
    # Mapeia a URL raiz ('') para a view 'index' do módulo 
    # 'views' com o nome 'index'
    path('', views.index, name='index'),
]