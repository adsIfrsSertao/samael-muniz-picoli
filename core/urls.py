from django.urls import path

from core import views


app_name = 'core'

urlpatterns = [
    # Mapeia a URL raiz ('') para a view 'index' do módulo
    # 'views' com o nome 'index'
    path('', views.index, name='index'),
]
