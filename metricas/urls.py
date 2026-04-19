
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_metricas, name='dashboard_metricas'),
    path('conectar/', views.conectar_instagram, name='conectar_instagram'),
    path('salvar-token/', views.salvar_token, name='salvar_token'),
    path('atualizar/<int:pk>/', views.atualizar_metricas, name='atualizar_metricas'),
    path('detalhe/<int:pk>/', views.detalhe_metricas, name='detalhe_metricas'),
]