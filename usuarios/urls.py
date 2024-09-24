from django.urls import path

from usuarios import views


app_name = 'usuarios'

urlpatterns = [
    path('registrar/', views.CadastrarUsuario.as_view(), name = 'registrar'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    
]