from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Conteudo, RedeSocial
from crm.models import Cliente
from django.contrib.auth.models import User

@login_required
def lista_conteudos(request):
    conteudos = Conteudo.objects.all().order_by('-data_publicacao')
    clientes = Cliente.objects.filter(status='ativo')
    responsaveis = User.objects.all()
    return render(request, 'conteudo/lista_conteudos.html', {
        'conteudos': conteudos,
        'clientes': clientes,
        'responsaveis': responsaveis,
    })

@login_required
def novo_conteudo(request):
    if request.method == 'POST':
        cliente = Cliente.objects.get(pk=request.POST['cliente'])
        rede = RedeSocial.objects.filter(
            cliente=cliente,
            rede=request.POST['rede_social']
        ).first()
        Conteudo.objects.create(
            titulo=request.POST['titulo'],
            cliente=cliente,
            rede_social=rede,
            formato=request.POST['formato'],
            status=request.POST['status'],
            responsavel=User.objects.get(pk=request.POST['responsavel']) if request.POST.get('responsavel') else None,
            data_publicacao=request.POST['data_publicacao'] or None,
            legenda=request.POST.get('legenda', ''),
            observacoes=request.POST.get('observacoes', ''),
        )
        messages.success(request, 'Conteúdo criado com sucesso!')
        return redirect('lista_conteudos')
    clientes = Cliente.objects.filter(status='ativo')
    responsaveis = User.objects.all()
    return render(request, 'conteudo/novo_conteudo.html', {
        'clientes': clientes,
        'responsaveis': responsaveis,
    })

@login_required
def detalhe_conteudo(request, pk):
    conteudo = get_object_or_404(Conteudo, pk=pk)
    return render(request, 'conteudo/detalhe_conteudo.html', {'conteudo': conteudo})

@login_required
def editar_conteudo(request, pk):
    conteudo = get_object_or_404(Conteudo, pk=pk)
    if request.method == 'POST':
        conteudo.titulo = request.POST['titulo']
        conteudo.formato = request.POST['formato']
        conteudo.status = request.POST['status']
        conteudo.data_publicacao = request.POST['data_publicacao'] or None
        conteudo.legenda = request.POST.get('legenda', '')
        conteudo.observacoes = request.POST.get('observacoes', '')
        conteudo.save()
        messages.success(request, 'Conteúdo atualizado!')
        return redirect('detalhe_conteudo', pk=pk)
    clientes = Cliente.objects.filter(status='ativo')
    responsaveis = User.objects.all()
    return render(request, 'conteudo/editar_conteudo.html', {
        'conteudo': conteudo,
        'clientes': clientes,
        'responsaveis': responsaveis,
    })

@login_required
def calendario(request):
    conteudos = Conteudo.objects.exclude(data_publicacao=None).order_by('data_publicacao')
    eventos = []
    for c in conteudos:
        cor = {
            'instagram': '#E1306C',
            'facebook': '#1877F2',
            'linkedin': '#0A66C2',
            'tiktok': '#010101',
            'youtube': '#FF0000',
            'twitter': '#1DA1F2',
        }.get(c.rede_social.rede if c.rede_social else '', '#F59E0B')
        eventos.append({
            'title': f"{c.titulo} ({c.cliente.nome})",
            'date': c.data_publicacao.strftime('%Y-%m-%dT%H:%M:%S') if c.data_publicacao else '',
            'color': cor,
            'url': f'/conteudo/{c.pk}/',
        })
    import json
    return render(request, 'conteudo/calendario.html', {
        'eventos_json': json.dumps(eventos)
    })