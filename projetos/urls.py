from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_projetos, name='lista_projetos'),
    path('novo/', views.novo_projeto, name='novo_projeto'),
    path('<int:pk>/', views.detalhe_projeto, name='detalhe_projeto'),
    path('<int:pk>/editar/', views.editar_projeto, name='editar_projeto'),
    path('<int:pk>/tarefa/', views.nova_tarefa, name='nova_tarefa'),
    path('tarefa/<int:pk>/atualizar/', views.atualizar_tarefa, name='atualizar_tarefa'),
    path('tarefa/<int:pk>/deletar/', views.deletar_tarefa, name='deletar_tarefa'),
]