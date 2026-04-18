from django.db import models

class Cliente(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('prospecto', 'Prospecto'),
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]
    
    nome = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    data_entrada = models.DateTimeField(auto_now_add=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contatos')
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    proximo_contato = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Contato com {self.cliente.nome} em {self.data.strftime('%d/%m/%Y')}"
