from django.urls import path

from graficos import views

app_name = 'graficos'

urlpatterns = [
    path('', views.gerar_grafico, name='gerar_grafico'),
]
