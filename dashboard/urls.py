from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('tarefa/<int:pk>/concluir/', views.concluir_tarefa, name='concluir_tarefa_dashboard'),
]