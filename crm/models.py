
from django.db import models

class Cliente(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('prospecto', 'Prospecto'),
        ('ativo', 'Ativo'),
        ('ouro', '⭐ Cliente Ouro'),
        ('inativo', 'Inativo'),
    ]
    SEGMENTO_CHOICES = [
        ('moda', 'Moda e Beleza'),
        ('saude', 'Saúde e Bem-estar'),
        ('alimentacao', 'Alimentação'),
        ('tecnologia', 'Tecnologia'),
        ('educacao', 'Educação'),
        ('imobiliario', 'Imobiliário'),
        ('varejo', 'Varejo'),
        ('servicos', 'Serviços'),
        ('outro', 'Outro'),
    ]

    # Dados básicos
    nome = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    data_entrada = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)

    # Dados pessoais
    cpf_cnpj = models.CharField(max_length=20, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=300, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)

    # Dados de negócio
    segmento = models.CharField(max_length=20, choices=SEGMENTO_CHOICES, blank=True)
    site = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    tiktok = models.CharField(max_length=100, blank=True)

    # Briefing
    briefing_completo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contatos')
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    proximo_contato = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Contato com {self.cliente.nome} em {self.data.strftime('%d/%m/%Y')}"

class Briefing(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='briefing')

    # Sobre o negócio
    descricao_negocio = models.TextField(blank=True)
    tempo_mercado = models.CharField(max_length=100, blank=True)
    diferenciais = models.TextField(blank=True)
    produtos_servicos = models.TextField(blank=True)
    ticket_medio = models.CharField(max_length=100, blank=True)

    # Público-alvo
    publico_idade = models.CharField(max_length=100, blank=True)
    publico_genero = models.CharField(max_length=50, blank=True)
    publico_localizacao = models.CharField(max_length=200, blank=True)
    publico_interesses = models.TextField(blank=True)
    publico_dores = models.TextField(blank=True)

    # Objetivos
    objetivo_principal = models.TextField(blank=True)
    meta_seguidores = models.CharField(max_length=100, blank=True)
    meta_faturamento = models.CharField(max_length=100, blank=True)

    # Concorrentes
    concorrentes = models.TextField(blank=True)
    referencias_visuais = models.TextField(blank=True)

    # Tom e estilo
    tom_comunicacao = models.CharField(max_length=200, blank=True)
    cores_marca = models.CharField(max_length=200, blank=True)
    evitar = models.TextField(blank=True)

    # Histórico
    ja_fez_marketing = models.BooleanField(default=False)
    o_que_funcionou = models.TextField(blank=True)
    o_que_nao_funcionou = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Briefing - {self.cliente.nome}"