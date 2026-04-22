from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import Estrategia, MensagemEstrategia, TrintaEmUm
from crm.models import Cliente
from openai import OpenAI
from django.utils import timezone
import json
from datetime import date

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """Você é Primo, o especialista em marketing digital da agência Primordial.
Você é um estrategista sênior com profundo conhecimento em:
- Estratégias de redes sociais (Instagram, TikTok, LinkedIn, Facebook, YouTube)
- Criação de conteúdo e roteiros criativos
- Marketing de conteúdo e inbound marketing
- Branding e posicionamento de marca
- Tendências atuais do mercado digital brasileiro
- Metodologia 30 em 1: criar 30 dias de conteúdo em um único dia

Seu papel é conversar com a equipe da Primordial para desenvolver estratégias personalizadas.
Ao iniciar uma conversa:
1. Pergunte sobre o cliente (nicho, público-alvo, objetivos)
2. Entenda os desafios e oportunidades
3. Desenvolva a estratégia de forma colaborativa
4. Ao final, gere um documento completo e profissional
Responda sempre em português brasileiro."""

SYSTEM_PROMPT_30EM1 = """Você é Primo, especialista em marketing digital da Primordial.
Sua missão agora é desenvolver o planejamento completo do método 30 em 1 para o cliente informado.

O método 30 em 1 consiste em:
- Criar 30 dias de conteúdo em um único dia de produção
- Dividir o mês em temas semanais
- Planejar formatos variados (Reels, Posts, Stories, Carrosséis)
- Definir legendas, hashtags e CTAs para cada conteúdo
- Alinhar com os objetivos estratégicos do cliente

Siga este fluxo:
1. Pergunte sobre o mês de referência e objetivos
2. Defina os 4 temas semanais
3. Crie o calendário completo com 30 conteúdos
4. Gere o documento final organizado por semana

Responda sempre em português brasileiro."""

def get_semana_do_mes():
    hoje = date.today()
    dia = hoje.day
    if dia <= 7:
        return 1
    elif dia <= 14:
        return 2
    elif dia <= 21:
        return 3
    else:
        return 4

@login_required
def lista_estrategias(request):
    estrategias = Estrategia.objects.all()
    clientes = Cliente.objects.filter(status__in=['ativo', 'ouro'])
    semana_atual = get_semana_do_mes()

    # Semana 3 — clientes sem estratégia do mês
    alertas_estrategia = []
    if semana_atual == 3:
        mes_atual = date.today().replace(day=1)
        clientes_ativos = Cliente.objects.filter(status__in=['ativo', 'ouro'])
        for c in clientes_ativos:
            tem_estrategia = Estrategia.objects.filter(
                cliente=c,
                mes_referencia__month=date.today().month,
                mes_referencia__year=date.today().year,
            ).exists()
            if not tem_estrategia:
                alertas_estrategia.append(c)

    # Semana 4 — clientes ouro sem 30em1 do mês
    alertas_30em1 = []
    if semana_atual == 4:
        clientes_ouro = Cliente.objects.filter(status='ouro')
        for c in clientes_ouro:
            tem_30em1 = TrintaEmUm.objects.filter(
                cliente=c,
                mes_referencia__month=date.today().month,
                mes_referencia__year=date.today().year,
            ).exists()
            if not tem_30em1:
                alertas_30em1.append(c)

    return render(request, 'estrategia/lista.html', {
        'estrategias': estrategias,
        'clientes': clientes,
        'semana_atual': semana_atual,
        'alertas_estrategia': alertas_estrategia,
        'alertas_30em1': alertas_30em1,
    })

@login_required
def nova_estrategia(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = Cliente.objects.get(pk=cliente_id) if cliente_id else None
        mes_ref = request.POST.get('mes_referencia') or None
        tipo = request.POST['tipo']

        estrategia = Estrategia.objects.create(
            titulo=request.POST['titulo'],
            tipo=tipo,
            cliente=cliente,
            mes_referencia=mes_ref,
            criado_por=request.user,
        )

        system = SYSTEM_PROMPT_30EM1 if tipo == '30_em_1' else SYSTEM_PROMPT
        cliente_nome = cliente.nome if cliente else 'não especificado'
        tipo_label = dict(Estrategia.TIPO_CHOICES).get(tipo, '')

        primeiro_prompt = f"Olá! Vou desenvolver uma estratégia de {tipo_label} para o cliente {cliente_nome}. Me conte mais sobre esse cliente para começarmos."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": primeiro_prompt}
            ]
        )
        resposta_ia = response.choices[0].message.content
        MensagemEstrategia.objects.create(
            estrategia=estrategia,
            role='assistant',
            conteudo=resposta_ia,
        )
        return redirect('chat_estrategia', pk=estrategia.pk)

    clientes = Cliente.objects.filter(status__in=['ativo', 'ouro'])
    return render(request, 'estrategia/nova.html', {'clientes': clientes})

@login_required
def chat_estrategia(request, pk):
    estrategia = get_object_or_404(Estrategia, pk=pk)
    mensagens = estrategia.mensagens.all()
    return render(request, 'estrategia/chat.html', {
        'estrategia': estrategia,
        'mensagens': mensagens,
    })

@login_required
def enviar_mensagem(request, pk):
    if request.method == 'POST':
        estrategia = get_object_or_404(Estrategia, pk=pk)
        data = json.loads(request.body)
        mensagem_usuario = data.get('mensagem', '')

        MensagemEstrategia.objects.create(
            estrategia=estrategia,
            role='user',
            conteudo=mensagem_usuario,
        )

        system = SYSTEM_PROMPT_30EM1 if estrategia.tipo == '30_em_1' else SYSTEM_PROMPT
        historico = [{"role": "system", "content": system}]
        for msg in estrategia.mensagens.all():
            historico.append({"role": msg.role, "content": msg.conteudo})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=historico
        )
        resposta_ia = response.choices[0].message.content

        MensagemEstrategia.objects.create(
            estrategia=estrategia,
            role='assistant',
            conteudo=resposta_ia,
        )

        return JsonResponse({'resposta': resposta_ia})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@login_required
def gerar_documento(request, pk):
    estrategia = get_object_or_404(Estrategia, pk=pk)
    mensagens = estrategia.mensagens.all()

    system = SYSTEM_PROMPT_30EM1 if estrategia.tipo == '30_em_1' else SYSTEM_PROMPT
    historico = [{"role": "system", "content": system}]
    for msg in mensagens:
        historico.append({"role": msg.role, "content": msg.conteudo})

    if estrategia.tipo == '30_em_1':
        prompt_final = """Com base em tudo que conversamos, gere agora o documento completo do planejamento 30 em 1.
        O documento deve ter:
        1. Resumo Estratégico do Mês
        2. Temas por Semana
        3. Calendário Completo — 30 conteúdos organizados por dia
           Para cada conteúdo: Dia, Formato, Tema, Título, Legenda resumida, CTA
        4. Hashtags recomendadas
        5. Observações finais
        Formate bem com títulos e subtítulos claros."""
    else:
        prompt_final = """Com base em tudo que conversamos, gere agora um documento completo e profissional da estratégia.
        O documento deve ter:
        1. Resumo Executivo
        2. Análise do Cliente e Mercado
        3. Objetivos e Metas
        4. Estratégia Detalhada
        5. Plano de Ação
        6. Métricas de Sucesso
        Formate bem com títulos e subtítulos claros."""

    historico.append({"role": "user", "content": prompt_final})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=historico,
        max_tokens=3000,
    )
    documento = response.choices[0].message.content

    estrategia.documento_final = documento
    estrategia.status = 'finalizada'
    estrategia.save()

    messages.success(request, 'Documento gerado com sucesso!')
    return redirect('detalhe_estrategia', pk=pk)

@login_required
def detalhe_estrategia(request, pk):
    estrategia = get_object_or_404(Estrategia, pk=pk)
    return render(request, 'estrategia/detalhe.html', {'estrategia': estrategia})

@login_required
def lista_30em1(request):
    mes_atual = date.today().replace(day=1)
    registros = TrintaEmUm.objects.filter(
        mes_referencia__month=date.today().month,
        mes_referencia__year=date.today().year,
    ).select_related('cliente', 'estrategia')
    clientes_ouro = Cliente.objects.filter(status='ouro')
    return render(request, 'estrategia/30em1.html', {
        'registros': registros,
        'clientes_ouro': clientes_ouro,
        'mes_atual': date.today(),
    })

@login_required
def criar_30em1(request):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, pk=request.POST['cliente'])
        mes_ref = request.POST['mes_referencia']
        TrintaEmUm.objects.get_or_create(
            cliente=cliente,
            mes_referencia=mes_ref,
            defaults={'status': 'reuniao_agendada' if request.POST.get('data_reuniao') else 'pendente'}
        )
        messages.success(request, f'30 em 1 criado para {cliente.nome}!')
        return redirect('lista_30em1')
    return redirect('lista_30em1')

@login_required
def atualizar_30em1(request, pk):
    registro = get_object_or_404(TrintaEmUm, pk=pk)
    if request.method == 'POST':
        registro.status = request.POST['status']
        registro.data_reuniao = request.POST.get('data_reuniao') or None
        registro.observacoes = request.POST.get('observacoes', '')
        if request.POST.get('estrategia_id'):
            registro.estrategia = get_object_or_404(Estrategia, pk=request.POST['estrategia_id'])
        registro.save()
        messages.success(request, 'Atualizado com sucesso!')
    return redirect('lista_30em1')