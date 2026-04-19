from django.db import models
from django.contrib.auth.models import User
from crm.models import Cliente

class Estrategia(models.Model):
    TIPO_CHOICES = [
        ('redes_sociais', 'Redes Sociais'),
        ('conteudo', 'Conteúdo'),
        ('marketing_completo', 'Marketing Completo'),
        ('roteiro', 'Roteiro'),
    ]
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('finalizada', 'Finalizada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='estrategias', null=True, blank=True)
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    documento_final = models.TextField(blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"

class MensagemEstrategia(models.Model):
    ROLE_CHOICES = [
        ('user', 'Usuário'),
        ('assistant', 'IA'),
    ]

    estrategia = models.ForeignKey(Estrategia, on_delete=models.CASCADE, related_name='mensagens')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']

    def __str__(self):
        return f"{self.role} - {self.estrategia.titulo}"