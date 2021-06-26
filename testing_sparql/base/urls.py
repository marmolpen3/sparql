from django.urls import path
from base import views as views


urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'),
    path('cantantes/', views.BuscarCantantesView.as_view(), name='buscar_cantantes'),
    path('cantante/<cantante_nombre>/', views.PerfilCantanteView.as_view(), name='perfil_cantante'),
]
