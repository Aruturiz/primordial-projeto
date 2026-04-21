from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from crm.models import Cliente
from projetos.models import Projeto, Tarefa
from conteudo.models import Conteudo
from django.utils import timezone

@login_required
def index(request):
    hoje = timezone.now()
    mes_atual = hoje.month
    ano_atual = hoje.year

    context = {
        'total_clientes': Cliente.objects.count(),
        'projetos_ativos': Projeto.objects.filter(status='em_andamento').count(),
        'minhas_tarefas_pendentes': Tarefa.objects.filter(
            responsavel=request.user,
            status__in=['pendente', 'em_andamento']
        ).count(),
        'tarefas_concluidas_mes': Tarefa.objects.filter(
            responsavel=request.user,
            status='concluida',
        ).count(),
        'minhas_tarefas': Tarefa.objects.filter(
            responsavel=request.user,
            status__in=['pendente', 'em_andamento']
        ).order_by('-id').select_related('projeto'),
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def concluir_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    tarefa.status = 'concluida'
    tarefa.save()
    messages.success(request, f'Tarefa "{tarefa.titulo}" concluída!')
    return redirect('dashboard')