from django.db import models
from crm.models import Cliente

class Campanha(models.Model):
    CANAL_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('email', 'E-mail Marketing'),
        ('outro', 'Outro'),
    ]

    nome = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='campanhas')
    canal = models.CharField(max_length=20, choices=CANAL_CHOICES)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    objetivo = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} - {self.cliente.nome}"

class Metrica(models.Model):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='metricas')
    data = models.DateField()
    alcance = models.IntegerField(default=0)
    impressoes = models.IntegerField(default=0)
    engajamento = models.IntegerField(default=0)
    cliques = models.IntegerField(default=0)
    seguidores_ganhos = models.IntegerField(default=0)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.campanha.nome} - {self.data.strftime('%d/%m/%Y')}"

class InstagramToken(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='instagram_token')
    access_token = models.TextField()
    instagram_account_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True)
    token_criado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Token Instagram - {self.cliente.nome}"

class InstagramMetrica(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='instagram_metricas')
    data_coleta = models.DateTimeField(auto_now_add=True)
    seguidores = models.IntegerField(default=0)
    alcance_7d = models.IntegerField(default=0)
    impressoes_7d = models.IntegerField(default=0)
    engajamento_7d = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-data_coleta']

    def __str__(self):
        return f"{self.cliente.nome} - {self.data_coleta.strftime('%d/%m/%Y')}"