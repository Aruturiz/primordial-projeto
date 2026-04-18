from django.db import models
from django.contrib.auth.models import User
from crm.models import Cliente

class Projeto(models.Model):
    STATUS_CHOICES = [
        ('planejamento', 'Planejamento'),
        ('em_andamento', 'Em Andamento'),
        ('pausado', 'Pausado'),
        ('concluido', 'Concluído'),
    ]

    nome = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejamento')
    data_inicio = models.DateField()
    data_prazo = models.DateField(null=True, blank=True)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
    ]

    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='tarefas')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    prazo = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo