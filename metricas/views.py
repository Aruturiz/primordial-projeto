from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from crm.models import Cliente
from .models import InstagramToken, InstagramMetrica, Campanha, Metrica
import requests

def get_instagram_account_id(access_token, page_id):
    url = f"https://graph.facebook.com/v18.0/{page_id}?fields=instagram_business_account&access_token={access_token}"
    r = requests.get(url).json()
    return r.get('instagram_business_account', {}).get('id')

def buscar_metricas_instagram(access_token, ig_account_id):
    dados = {}
    # Seguidores e info básica
    url = f"https://graph.facebook.com/v18.0/{ig_account_id}?fields=followers_count,media_count,username&access_token={access_token}"
    r = requests.get(url).json()
    dados['seguidores'] = r.get('followers_count', 0)
    dados['posts_count'] = r.get('media_count', 0)
    dados['username'] = r.get('username', '')

    # Insights 7 dias
    url_insights = f"https://graph.facebook.com/v18.0/{ig_account_id}/insights?metric=reach,impressions&period=day&since=-7days&access_token={access_token}"
    r2 = requests.get(url_insights).json()
    alcance = 0
    impressoes = 0
    if 'data' in r2:
        for item in r2['data']:
            if item['name'] == 'reach':
                alcance = sum(v['value'] for v in item.get('values', []))
            if item['name'] == 'impressions':
                impressoes = sum(v['value'] for v in item.get('values', []))
    dados['alcance_7d'] = alcance
    dados['impressoes_7d'] = impressoes
    return dados

@login_required
def dashboard_metricas(request):
    clientes_com_token = InstagramToken.objects.select_related('cliente').all()
    metricas_recentes = {}
    for token in clientes_com_token:
        metrica = InstagramMetrica.objects.filter(cliente=token.cliente).first()
        if metrica:
            metricas_recentes[token.cliente.id] = metrica
    return render(request, 'metricas/dashboard.html', {
        'clientes_com_token': clientes_com_token,
        'metricas_recentes': metricas_recentes,
    })

@login_required
def conectar_instagram(request):
    clientes = Cliente.objects.filter(status='ativo')
    return render(request, 'metricas/conectar.html', {'clientes': clientes})

@login_required
def salvar_token(request):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, pk=request.POST['cliente'])
        access_token = request.POST['access_token']
        page_id = request.POST['page_id']

        ig_account_id = get_instagram_account_id(access_token, page_id)
        if not ig_account_id:
            messages.error(request, 'Não foi possível encontrar a conta do Instagram. Verifique o Page ID e o Token.')
            return redirect('conectar_instagram')

        InstagramToken.objects.update_or_create(
            cliente=cliente,
            defaults={
                'access_token': access_token,
                'instagram_account_id': ig_account_id,
            }
        )
        messages.success(request, f'Instagram de {cliente.nome} conectado com sucesso!')
        return redirect('atualizar_metricas', pk=cliente.pk)
    return redirect('conectar_instagram')

@login_required
def atualizar_metricas(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    try:
        token = cliente.instagram_token
        dados = buscar_metricas_instagram(token.access_token, token.instagram_account_id)
        InstagramMetrica.objects.create(
            cliente=cliente,
            seguidores=dados['seguidores'],
            alcance_7d=dados['alcance_7d'],
            impressoes_7d=dados['impressoes_7d'],
            posts_count=dados['posts_count'],
        )
        if dados.get('username'):
            token.username = dados['username']
            token.save()
        messages.success(request, f'Métricas de {cliente.nome} atualizadas!')
    except Exception as e:
        messages.error(request, f'Erro ao buscar métricas: {str(e)}')
    return redirect('dashboard_metricas')

@login_required
def detalhe_metricas(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    metricas = InstagramMetrica.objects.filter(cliente=cliente)
    token = InstagramToken.objects.filter(cliente=cliente).first()
    return render(request, 'metricas/detalhe.html', {
        'cliente': cliente,
        'metricas': metricas,
        'token': token,
    })