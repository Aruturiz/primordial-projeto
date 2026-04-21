from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, Contato, Briefing
from django.contrib.auth.models import User
from projetos.models import Projeto
from conteudo.models import Conteudo
from metricas.models import InstagramMetrica

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-data_entrada')
    return render(request, 'crm/lista_clientes.html', {'clientes': clientes})

@login_required
def detalhe_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    contatos = cliente.contatos.all().order_by('-data')
    projetos = Projeto.objects.filter(cliente=cliente)
    conteudos = Conteudo.objects.filter(cliente=cliente).order_by('-data_publicacao')[:10]
    metricas = InstagramMetrica.objects.filter(cliente=cliente).first()
    briefing = Briefing.objects.filter(cliente=cliente).first()
    return render(request, 'crm/detalhe_cliente.html', {
        'cliente': cliente,
        'contatos': contatos,
        'projetos': projetos,
        'conteudos': conteudos,
        'metricas': metricas,
        'briefing': briefing,
    })

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        cliente = Cliente.objects.create(
            nome=request.POST['nome'],
            empresa=request.POST.get('empresa', ''),
            email=request.POST['email'],
            telefone=request.POST.get('telefone', ''),
            status=request.POST['status'],
            cpf_cnpj=request.POST.get('cpf_cnpj', ''),
            data_nascimento=request.POST.get('data_nascimento') or None,
            endereco=request.POST.get('endereco', ''),
            cidade=request.POST.get('cidade', ''),
            estado=request.POST.get('estado', ''),
            segmento=request.POST.get('segmento', ''),
            site=request.POST.get('site', ''),
            instagram=request.POST.get('instagram', ''),
            facebook=request.POST.get('facebook', ''),
            linkedin=request.POST.get('linkedin', ''),
            tiktok=request.POST.get('tiktok', ''),
            observacoes=request.POST.get('observacoes', ''),
        )
        messages.success(request, 'Cliente cadastrado! Agora preencha o briefing.')
        return redirect('briefing_cliente', pk=cliente.pk)
    return render(request, 'crm/novo_cliente.html')

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nome = request.POST['nome']
        cliente.empresa = request.POST.get('empresa', '')
        cliente.email = request.POST['email']
        cliente.telefone = request.POST.get('telefone', '')
        cliente.status = request.POST['status']
        cliente.cpf_cnpj = request.POST.get('cpf_cnpj', '')
        cliente.data_nascimento = request.POST.get('data_nascimento') or None
        cliente.endereco = request.POST.get('endereco', '')
        cliente.cidade = request.POST.get('cidade', '')
        cliente.estado = request.POST.get('estado', '')
        cliente.segmento = request.POST.get('segmento', '')
        cliente.site = request.POST.get('site', '')
        cliente.instagram = request.POST.get('instagram', '')
        cliente.facebook = request.POST.get('facebook', '')
        cliente.linkedin = request.POST.get('linkedin', '')
        cliente.tiktok = request.POST.get('tiktok', '')
        cliente.observacoes = request.POST.get('observacoes', '')
        cliente.save()
        messages.success(request, 'Cliente atualizado!')
        return redirect('detalhe_cliente', pk=pk)
    return render(request, 'crm/editar_cliente.html', {'cliente': cliente})

@login_required
def novo_contato(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        Contato.objects.create(
            cliente=cliente,
            descricao=request.POST['descricao'],
            proximo_contato=request.POST['proximo_contato'] or None,
        )
        messages.success(request, 'Contato registrado!')
    return redirect('detalhe_cliente', pk=pk)

@login_required
def briefing_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    briefing, created = Briefing.objects.get_or_create(cliente=cliente)
    if request.method == 'POST':
        briefing.descricao_negocio = request.POST.get('descricao_negocio', '')
        briefing.tempo_mercado = request.POST.get('tempo_mercado', '')
        briefing.diferenciais = request.POST.get('diferenciais', '')
        briefing.produtos_servicos = request.POST.get('produtos_servicos', '')
        briefing.ticket_medio = request.POST.get('ticket_medio', '')
        briefing.publico_idade = request.POST.get('publico_idade', '')
        briefing.publico_genero = request.POST.get('publico_genero', '')
        briefing.publico_localizacao = request.POST.get('publico_localizacao', '')
        briefing.publico_interesses = request.POST.get('publico_interesses', '')
        briefing.publico_dores = request.POST.get('publico_dores', '')
        briefing.objetivo_principal = request.POST.get('objetivo_principal', '')
        briefing.meta_seguidores = request.POST.get('meta_seguidores', '')
        briefing.meta_faturamento = request.POST.get('meta_faturamento', '')
        briefing.concorrentes = request.POST.get('concorrentes', '')
        briefing.referencias_visuais = request.POST.get('referencias_visuais', '')
        briefing.tom_comunicacao = request.POST.get('tom_comunicacao', '')
        briefing.cores_marca = request.POST.get('cores_marca', '')
        briefing.evitar = request.POST.get('evitar', '')
        briefing.ja_fez_marketing = request.POST.get('ja_fez_marketing') == 'on'
        briefing.o_que_funcionou = request.POST.get('o_que_funcionou', '')
        briefing.o_que_nao_funcionou = request.POST.get('o_que_nao_funcionou', '')
        briefing.save()
        cliente.briefing_completo = True
        cliente.save()
        messages.success(request, 'Briefing salvo com sucesso!')
        return redirect('detalhe_cliente', pk=pk)
    return render(request, 'crm/briefing.html', {
        'cliente': cliente,
        'briefing': briefing,
    })