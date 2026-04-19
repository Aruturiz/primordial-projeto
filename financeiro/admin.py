from django.contrib import admin
from .models import AcessoFinanceiro, Mensalidade, Transacao

admin.site.register(AcessoFinanceiro)
admin.site.register(Mensalidade)
admin.site.register(Transacao)