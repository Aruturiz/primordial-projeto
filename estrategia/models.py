from django.db import models
from django.contrib.auth.models import User
from crm.models import Cliente

class Estrategia(models.Model):
    TIPO_CHOICES = [
        ('redes_sociais', 'Redes Sociais'),
        ('conteudo', 'Conteúdo'),
        ('marketing_completo', 'Marketing Completo'),
        ('roteiro', 'Roteiro'),
        ('30_em_1', '30 em 1'),
    ]
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('finalizada', 'Finalizada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='estrategias', null=True, blank=True)
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    mes_referencia = models.DateField(null=True, blank=True)
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

class TrintaEmUm(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('reuniao_agendada', 'Reunião Agendada'),
        ('em_desenvolvimento', 'Em Desenvolvimento'),
        ('finalizado', 'Finalizado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='trinta_em_um')
    mes_referencia = models.DateField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pendente')
    data_reuniao = models.DateTimeField(null=True, blank=True)
    estrategia = models.ForeignKey(Estrategia, on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-mes_referencia']
        unique_together = ['cliente', 'mes_referencia']

    def __str__(self):
        return f"30em1 - {self.cliente.nome} - {self.mes_referencia.strftime('%m/%Y')}"