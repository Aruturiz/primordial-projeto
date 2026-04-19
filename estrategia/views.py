from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Estrategia, MensagemEstrategia
from crm.models import Cliente
from openai import OpenAI
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """Você é Primo, o especialista em marketing digital da agência Primordial. 
Você é um estrategista sênior com profundo conhecimento em:
- Estratégias de redes sociais (Instagram, TikTok, LinkedIn, Facebook, YouTube)
- Criação de conteúdo e roteiros criativos
- Marketing de conteúdo e inbound marketing
- Branding e posicionamento de marca
- Tendências atuais do mercado digital brasileiro

Seu papel é conversar com a equipe da Primordial para desenvolver estratégias personalizadas para os clientes da agência.

Ao iniciar uma conversa:
1. Pergunte sobre o cliente (nicho, público-alvo, objetivos)
2. Entenda os desafios e oportunidades
3. Desenvolva a estratégia de forma colaborativa
4. Ao final, gere um documento completo e profissional

Seja direto, criativo e sempre baseie suas sugestões em dados e tendências reais do mercado.
Responda sempre em português brasileiro."""

@login_required
def lista_estrategias(request):
    estrategias = Estrategia.objects.all()
    clientes = Cliente.objects.filter(status='ativo')
    return render(request, 'estrategia/lista.html', {
        'estrategias': estrategias,
        'clientes': clientes,
    })

@login_required
def nova_estrategia(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        estrategia = Estrategia.objects.create(
            titulo=request.POST['titulo'],
            tipo=request.POST['tipo'],
            cliente=Cliente.objects.get(pk=cliente_id) if cliente_id else None,
            criado_por=request.user,
        )
        # Mensagem inicial da IA
        tipo_label = dict(Estrategia.TIPO_CHOICES).get(estrategia.tipo, '')
        cliente_nome = estrategia.cliente.nome if estrategia.cliente else 'não especificado'
        
        primeiro_prompt = f"Olá! Vou desenvolver uma estratégia de {tipo_label} para o cliente {cliente_nome}. Me conte mais sobre esse cliente para começarmos."
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
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
    clientes = Cliente.objects.filter(status='ativo')
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

        # Salva mensagem do usuário
        MensagemEstrategia.objects.create(
            estrategia=estrategia,
            role='user',
            conteudo=mensagem_usuario,
        )

        # Monta histórico para a IA
        historico = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in estrategia.mensagens.all():
            historico.append({
                "role": msg.role,
                "content": msg.conteudo,
            })

        # Chama a OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=historico
        )
        resposta_ia = response.choices[0].message.content

        # Salva resposta da IA
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

    historico = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in mensagens:
        historico.append({"role": msg.role, "content": msg.conteudo})

    historico.append({
        "role": "user",
        "content": """Com base em tudo que conversamos, gere agora um documento completo e profissional da estratégia.
        O documento deve ter:
        1. Resumo Executivo
        2. Análise do Cliente e Mercado
        3. Objetivos e Metas
        4. Estratégia Detalhada
        5. Plano de Ação
        6. Métricas de Sucesso
        Formate bem o documento com títulos e subtítulos claros."""
    })

    response = client.chat.completions.create(
        model="gpt-4",
        messages=historico,
        max_tokens=2000,
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