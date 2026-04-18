from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import TextoSite, Evento, FotoGaleria, FotoConvidado, FotoFormanda


def _textos():
    """Retorna dicionário com todos os textos configuráveis."""
    defaults = {
        'hero_titulo': 'Micaelle',
        'hero_subtitulo': 'Bacharel em Direito · Universidade de Caxias do Sul — UCS · Turma 2026',
        'historia_titulo': 'Uma história de determinação',
        'historia_corpo': (
            'De <strong>Alegrete</strong>, interior do Rio Grande do Sul, Micaelle trouxe consigo '
            'uma força que poucas pessoas carregam tão jovem: a capacidade de enfrentar os próprios '
            'desafios sem recuar.\n\n'
            'Responsável e independente desde cedo, ela construiu seu caminho com as próprias mãos — '
            'e foi no <strong>Direito</strong> que encontrou sua vocação. A paixão pelo '
            '<strong>Direito Civil</strong>, especialmente pelo Direito de Família, não é apenas uma '
            'escolha acadêmica: é um reflexo de quem ela é — alguém que acredita nas relações humanas '
            'e na justiça como pilares da vida.\n\n'
            'Cinco anos depois, o diploma não é apenas um papel. É o símbolo de cada madrugada '
            'estudada, de cada obstáculo superado, e da certeza de que o esforço sempre tem um destino.'
        ),
        'agradecimento_frase': (
            '"Nenhuma conquista se constrói sozinha. Este diploma carrega o nome de todos que '
            'acreditaram em mim quando eu mais precisei — e de alguns que nunca deixaram de estar '
            'ao meu lado."'
        ),
        'agradecimento_homenageados': 'Meu Pai\nMinha Avó\nMeu Namorado\nMeu Melhor Colega\nMeus Professores\nToda a Família',
        'envio_descricao': 'Tem uma memória especial com ela? Compartilhe aqui e faça parte desta galeria!',
    }
    textos = {}
    for obj in TextoSite.objects.all():
        textos[obj.secao] = obj.conteudo
    for key, val in defaults.items():
        if key not in textos:
            textos[key] = val
    return textos


def home(request):
    textos = _textos()
    eventos = Evento.objects.filter(ativo=True)
    fotos_galeria = FotoGaleria.objects.filter(ativa=True)
    fotos_convidados = FotoConvidado.objects.filter(aprovada=True)

    homenageados = [
        h.strip()
        for h in textos.get('agradecimento_homenageados', '').splitlines()
        if h.strip()
    ]

    paragrafos_historia = [
        p.strip()
        for p in textos.get('historia_corpo', '').split('\n\n')
        if p.strip()
    ]

    foto_formanda = FotoFormanda.objects.first()

    context = {
        'textos': textos,
        'eventos': {e.tipo: e for e in eventos},
        'fotos_galeria': fotos_galeria,
        'fotos_convidados': fotos_convidados,
        'homenageados': homenageados,
        'paragrafos_historia': paragrafos_historia,
        'foto_formanda': foto_formanda,
    }
    return render(request, 'core/home.html', context)


@require_POST
def enviar_foto(request):
    nome = request.POST.get('nome', '').strip()
    relacionamento = request.POST.get('relacionamento', '').strip()
    mensagem = request.POST.get('mensagem', '').strip()
    imagem = request.FILES.get('imagem')

    if not nome:
        return JsonResponse({'ok': False, 'erro': 'Por favor, informe seu nome.'}, status=400)
    if not imagem:
        return JsonResponse({'ok': False, 'erro': 'Por favor, selecione uma foto.'}, status=400)

    tipos_permitidos = ['image/jpeg', 'image/png', 'image/heic', 'image/webp']
    if imagem.content_type not in tipos_permitidos:
        return JsonResponse({'ok': False, 'erro': 'Formato de imagem não suportado.'}, status=400)

    if imagem.size > 15 * 1024 * 1024:
        return JsonResponse({'ok': False, 'erro': 'A foto é muito grande. Máximo 15MB.'}, status=400)

    foto = FotoConvidado.objects.create(
        nome=nome,
        relacionamento=relacionamento,
        mensagem=mensagem,
        imagem=imagem,
        aprovada=False,
    )
    return JsonResponse({
        'ok': True,
        'mensagem': 'Foto enviada com sucesso! Ela aparecerá na galeria após aprovação. 💛',
    })


def galeria_api(request):
    """Retorna fotos aprovadas de convidados para atualização da galeria."""
    fotos = FotoConvidado.objects.filter(aprovada=True).values(
        'id', 'nome', 'relacionamento', 'imagem'
    )
    data = []
    for f in fotos:
        data.append({
            'id': f['id'],
            'nome': f['nome'],
            'relacionamento': f['relacionamento'],
            'url': request.build_absolute_uri(f'/media/{f["imagem"]}'),
        })
    return JsonResponse({'fotos': data})
