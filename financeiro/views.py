from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Mensalidade, Transacao, AcessoFinanceiro
from crm.models import Cliente

def tem_acesso_financeiro(user):
    if user.is_superuser:
        return True
    try:
        return user.acessofinanceiro.autorizado
    except:
        return False

@login_required
def dashboard_financeiro(request):
    if not tem_acesso_financeiro(request.user):
        messages.error(request, 'Acesso negado ao módulo financeiro.')
        return redirect('dashboard')

    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year

    mensalidades_mes = Mensalidade.objects.filter(
        mes_referencia__month=mes_atual,
        mes_referencia__year=ano_atual
    )
    receitas_mes = Transacao.objects.filter(
        tipo='receita',
        data__month=mes_atual,
        data__year=ano_atual
    )
    despesas_mes = Transacao.objects.filter(
        tipo='despesa',
        data__month=mes_atual,
        data__year=ano_atual
    )

    total_receitas = sum(t.valor for t in receitas_mes) or Decimal('0')
    total_despesas = sum(t.valor for t in despesas_mes) or Decimal('0')
    saldo = total_receitas - total_despesas

    mensalidades_pagas = mensalidades_mes.filter(status='pago').count()
    mensalidades_pendentes = mensalidades_mes.filter(status='pendente').count()
    mensalidades_atrasadas = mensalidades_mes.filter(status='atrasado').count()

    context = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'mensalidades_pagas': mensalidades_pagas,
        'mensalidades_pendentes': mensalidades_pendentes,
        'mensalidades_atrasadas': mensalidades_atrasadas,
        'mensalidades_mes': mensalidades_mes,
        'transacoes_recentes': Transacao.objects.all()[:10],
    }
    return render(request, 'financeiro/dashboard.html', context)

@login_required
def lista_mensalidades(request):
    if not tem_acesso_financeiro(request.user):
        messages.error(request, 'Acesso negado ao módulo financeiro.')
        return redirect('dashboard')
    mensalidades = Mensalidade.objects.all()
    clientes = Cliente.objects.filter(status='ativo')
    return render(request, 'financeiro/mensalidades.html', {
        'mensalidades': mensalidades,
        'clientes': clientes
    })

@login_required
def registrar_pagamento(request, pk):
    if not tem_acesso_financeiro(request.user):
        return redirect('dashboard')
    mensalidade = get_object_or_404(Mensalidade, pk=pk)
    if request.method == 'POST':
        mensalidade.status = 'pago'
        mensalidade.data_pagamento = timezone.now().date()
        mensalidade.save()
        Transacao.objects.create(
            tipo='receita',
            categoria='mensalidade',
            descricao=f'Mensalidade {mensalidade.cliente.nome} - {mensalidade.mes_referencia.strftime("%m/%Y")}',
            valor=mensalidade.valor,
            data=timezone.now().date(),
            cliente=mensalidade.cliente,
            criado_por=request.user,
        )
        messages.success(request, 'Pagamento registrado com sucesso!')
    return redirect('lista_mensalidades')

@login_required
def nova_mensalidade(request):
    if not tem_acesso_financeiro(request.user):
        return redirect('dashboard')
    if request.method == 'POST':
        Mensalidade.objects.create(
            cliente=Cliente.objects.get(pk=request.POST['cliente']),
            valor=request.POST['valor'],
            mes_referencia=request.POST['mes_referencia'],
            observacoes=request.POST.get('observacoes', ''),
        )
        messages.success(request, 'Mensalidade criada com sucesso!')
        return redirect('lista_mensalidades')
    return redirect('lista_mensalidades')

@login_required
def lista_transacoes(request):
    if not tem_acesso_financeiro(request.user):
        messages.error(request, 'Acesso negado ao módulo financeiro.')
        return redirect('dashboard')
    transacoes = Transacao.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'financeiro/transacoes.html', {
        'transacoes': transacoes,
        'clientes': clientes
    })

@login_required
def nova_transacao(request):
    if not tem_acesso_financeiro(request.user):
        return redirect('dashboard')
    if request.method == 'POST':
        Transacao.objects.create(
            tipo=request.POST['tipo'],
            categoria=request.POST['categoria'],
            descricao=request.POST['descricao'],
            valor=request.POST['valor'],
            data=request.POST['data'],
            cliente=Cliente.objects.get(pk=request.POST['cliente']) if request.POST.get('cliente') else None,
            criado_por=request.user,
            observacoes=request.POST.get('observacoes', ''),
        )
        messages.success(request, 'Transação registrada!')
        return redirect('lista_transacoes')
    return redirect('lista_transacoes')

@login_required
def gerenciar_acessos(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    from django.contrib.auth.models import User
    usuarios = User.objects.exclude(is_superuser=True)
    acessos = AcessoFinanceiro.objects.all()
    if request.method == 'POST':
        user_id = request.POST['usuario']
        autorizado = request.POST.get('autorizado') == 'on'
        user = User.objects.get(pk=user_id)
        acesso, _ = AcessoFinanceiro.objects.get_or_create(usuario=user)
        acesso.autorizado = autorizado
        acesso.save()
        messages.success(request, 'Acesso atualizado!')
        return redirect('gerenciar_acessos')
    return render(request, 'financeiro/acessos.html', {
        'usuarios': usuarios,
        'acessos': acessos
    })