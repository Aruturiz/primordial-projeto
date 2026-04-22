from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_estrategias, name='lista_estrategias'),
    path('nova/', views.nova_estrategia, name='nova_estrategia'),
    path('<int:pk>/', views.chat_estrategia, name='chat_estrategia'),
    path('<int:pk>/enviar/', views.enviar_mensagem, name='enviar_mensagem'),
    path('<int:pk>/gerar-documento/', views.gerar_documento, name='gerar_documento'),
    path('<int:pk>/detalhe/', views.detalhe_estrategia, name='detalhe_estrategia'),
    path('30em1/', views.lista_30em1, name='lista_30em1'),
    path('30em1/criar/', views.criar_30em1, name='criar_30em1'),
    path('30em1/<int:pk>/atualizar/', views.atualizar_30em1, name='atualizar_30em1'),
]