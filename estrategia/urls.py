from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_estrategias, name='lista_estrategias'),
    path('nova/', views.nova_estrategia, name='nova_estrategia'),
    path('<int:pk>/', views.chat_estrategia, name='chat_estrategia'),
    path('<int:pk>/enviar/', views.enviar_mensagem, name='enviar_mensagem'),
    path('<int:pk>/gerar-documento/', views.gerar_documento, name='gerar_documento'),
    path('<int:pk>/detalhe/', views.detalhe_estrategia, name='detalhe_estrategia'),
]