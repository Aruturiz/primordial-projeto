from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_conteudos, name='lista_conteudos'),
    path('novo/', views.novo_conteudo, name='novo_conteudo'),
    path('calendario/', views.calendario, name='calendario'),
    path('<int:pk>/', views.detalhe_conteudo, name='detalhe_conteudo'),
    path('<int:pk>/editar/', views.editar_conteudo, name='editar_conteudo'),
]