"""projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.http import Http404
from django.urls import include, path


def has_permission(request):
    """
    Verifica se o usuário tem permissão para acessar um recurso.

    Este método verifica se o usuário está ativo e se é um superusuário.
    Se ambas as condições forem atendidas, retorna True. Caso contrário,
    levanta um Http404.

    Args:
        request: O objeto de requisição que contém informações sobre o
                 usuário que está fazendo a solicitação.

    Returns:
        bool: True se o usuário estiver ativo e for um superusuário.

    Raises:
        Http404: Se o usuário não atender aos critérios de permissão.
    """

    if request.user.is_active and request.user.is_superuser:
        return True
    raise Http404


admin.site.has_permission = has_permission

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('produtos/', include('produtos.urls')),
    path('clientes/', include('clientes.urls')),
    path('vendedores/', include('vendedores.urls')),
    path('vendas/', include('vendas.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('graficos/', include('graficos.urls')),
]
