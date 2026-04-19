from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Projeto, Tarefa
from crm.models import Cliente

@login_required
def lista_projetos(request):
    projetos = Projeto.objects.all().order_by('-id')
    return render(request, 'projetos/lista_projetos.html', {'projetos': projetos})

@login_required
def novo_projeto(request):
    if request.method == 'POST':
        Projeto.objects.create(
            nome=request.POST['nome'],
            cliente=Cliente.objects.get(pk=request.POST['cliente']) if request.POST.get('cliente') else None,
            descricao=request.POST.get('descricao', ''),
            status=request.POST['status'],
            data_inicio=request.POST['data_inicio'],
            data_prazo=request.POST['data_prazo'] or None,
            responsavel=User.objects.get(pk=request.POST['responsavel']) if request.POST.get('responsavel') else None,
        )
        messages.success(request, 'Projeto criado com sucesso!')
        return redirect('lista_projetos')
    clientes = Cliente.objects.filter(status='ativo')
    responsaveis = User.objects.all()
    return render(request, 'projetos/novo_projeto.html', {
        'clientes': clientes,
        'responsaveis': responsaveis,
    })

@login_required
def detalhe_projeto(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    tarefas = projeto.tarefas.all().order_by('status')
    responsaveis = User.objects.all()
    return render(request, 'projetos/detalhe_projeto.html', {
        'projeto': projeto,
        'tarefas': tarefas,
        'responsaveis': responsaveis,
    })

@login_required
def editar_projeto(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        projeto.nome = request.POST['nome']
        projeto.descricao = request.POST.get('descricao', '')
        projeto.status = request.POST['status']
        projeto.data_inicio = request.POST['data_inicio']
        projeto.data_prazo = request.POST['data_prazo'] or None
        projeto.responsavel = User.objects.get(pk=request.POST['responsavel']) if request.POST.get('responsavel') else None
        projeto.save()
        messages.success(request, 'Projeto atualizado!')
        return redirect('detalhe_projeto', pk=pk)
    clientes = Cliente.objects.filter(status='ativo')
    responsaveis = User.objects.all()
    return render(request, 'projetos/editar_projeto.html', {
        'projeto': projeto,
        'clientes': clientes,
        'responsaveis': responsaveis,
    })

@login_required
def nova_tarefa(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        Tarefa.objects.create(
            projeto=projeto,
            titulo=request.POST['titulo'],
            descricao=request.POST.get('descricao', ''),
            responsavel=User.objects.get(pk=request.POST['responsavel']) if request.POST.get('responsavel') else None,
            prioridade=request.POST['prioridade'],
            status=request.POST.get('status', 'pendente'),
            prazo=request.POST['prazo'] or None,
        )
        messages.success(request, 'Tarefa criada!')
        return redirect('detalhe_projeto', pk=pk)
    return redirect('detalhe_projeto', pk=pk)

@login_required
def atualizar_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == 'POST':
        tarefa.status = request.POST['status']
        tarefa.save()
        messages.success(request, 'Tarefa atualizada!')
    return redirect('detalhe_projeto', pk=tarefa.projeto.pk)

@login_required
def deletar_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    projeto_pk = tarefa.projeto.pk
    tarefa.delete()
    messages.success(request, 'Tarefa removida!')
    return redirect('detalhe_projeto', pk=projeto_pk)