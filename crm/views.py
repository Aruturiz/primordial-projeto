from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cliente, Contato
from django.contrib import messages

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-data_entrada')
    return render(request, 'crm/lista_clientes.html', {'clientes': clientes})

@login_required
def detalhe_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    contatos = cliente.contatos.all().order_by('-data')
    return render(request, 'crm/detalhe_cliente.html', {'cliente': cliente, 'contatos': contatos})

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nome=request.POST['nome'],
            empresa=request.POST['empresa'],
            email=request.POST['email'],
            telefone=request.POST['telefone'],
            status=request.POST['status'],
            observacoes=request.POST['observacoes'],
        )
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('lista_clientes')
    return render(request, 'crm/novo_cliente.html')

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
    return redirect('detalhe_cliente', pk=pk)

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nome = request.POST['nome']
        cliente.empresa = request.POST['empresa']
        cliente.email = request.POST['email']
        cliente.telefone = request.POST['telefone']
        cliente.status = request.POST['status']
        cliente.observacoes = request.POST['observacoes']
        cliente.save()
        messages.success(request, 'Cliente atualizado!')
        return redirect('detalhe_cliente', pk=pk)
    return render(request, 'crm/editar_cliente.html', {'cliente': cliente})