from django.db import models
from django.contrib.auth.models import User
from crm.models import Cliente

class AcessoFinanceiro(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {'Autorizado' if self.autorizado else 'Bloqueado'}"

class Mensalidade(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('atrasado', 'Atrasado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mensalidades')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    mes_referencia = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_pagamento = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ['-mes_referencia']

    def __str__(self):
        return f"{self.cliente.nome} - {self.mes_referencia.strftime('%m/%Y')} - {self.get_status_display()}"

class Transacao(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]
    CATEGORIA_CHOICES = [
        ('mensalidade', 'Mensalidade'),
        ('servico', 'Serviço Extra'),
        ('ferramenta', 'Ferramenta'),
        ('salario', 'Salário'),
        ('marketing', 'Marketing'),
        ('outro', 'Outro'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao} - R${self.valor}"