from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm.models import Cliente
from projetos.models import Projeto, Tarefa
from conteudo.models import Conteudo
from django.utils import timezone

@login_required
def index(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'projetos_ativos': Projeto.objects.filter(status='em_andamento').count(),
        'tarefas_concluidas': Tarefa.objects.filter(status='concluida').count(),
        'conteudos_mes': Conteudo.objects.filter(
            data_publicacao__month=timezone.now().month
        ).count(),
        'projetos_recentes': Projeto.objects.all().order_by('-id')[:5],
        'tarefas_pendentes': Tarefa.objects.filter(status='pendente').order_by('-id')[:5],
    }
    return render(request, 'dashboard/index.html', context)