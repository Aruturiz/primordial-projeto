from django.db import models
from django.contrib.auth.models import User
from crm.models import Cliente

class RedeSocial(models.Model):
    REDE_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter/X'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='redes_sociais')
    rede = models.CharField(max_length=20, choices=REDE_CHOICES)
    perfil = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.cliente.nome} - {self.rede}"

class Conteudo(models.Model):
    STATUS_CHOICES = [
        ('ideia', 'Ideia'),
        ('producao', 'Em Produção'),
        ('revisao', 'Em Revisão'),
        ('aprovado', 'Aprovado'),
        ('publicado', 'Publicado'),
    ]
    FORMATO_CHOICES = [
        ('post', 'Post'),
        ('reels', 'Reels'),
        ('stories', 'Stories'),
        ('carrossel', 'Carrossel'),
        ('video', 'Vídeo'),
        ('artigo', 'Artigo'),
    ]

    titulo = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='conteudos')
    rede_social = models.ForeignKey(RedeSocial, on_delete=models.SET_NULL, null=True, blank=True)
    formato = models.CharField(max_length=20, choices=FORMATO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ideia')
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_publicacao = models.DateTimeField(null=True, blank=True)
    legenda = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.titulo} - {self.cliente.nome}"