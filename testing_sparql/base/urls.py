from django.urls import path
from base import views as views


urlpatterns = [
    path('', views.InicioView.as_view(), name='inicio'),
]
