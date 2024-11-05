from django.urls import path

from usuarios import views

app_name = 'usuarios'

urlpatterns = [
    path('registrar/', views.CadastrarUsuario.as_view(), name='registrar'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('alterar-senha/', views.AlterarSenha.as_view(), name='alterar_senha'),
    path(
        'listar-usuarios/',
        views.ListarUsuarios.as_view(),
        name='listar_usuarios',
    ),
    path(
        '<int:pk>/deletar/',
        views.deletar_usuario,
        name='deletar_usuario',
    ),
]
