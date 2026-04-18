"""
Script para popular o banco com os dados iniciais.
Execute: python seed.py (após python manage.py migrate)
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'formatura.settings')
django.setup()

from formatura.core.models import TextoSite, Evento
from datetime import date, time

print("Populando textos do site...")
textos = [
    ('hero_titulo', 'Micaelle'),
    ('hero_subtitulo', 'Bacharel em Direito · Universidade de Caxias do Sul — UCS · Turma 2026'),
    ('historia_titulo', 'Uma história de determinação'),
    ('historia_corpo',
     'De <strong>Alegrete</strong>, interior do Rio Grande do Sul, Micaelle trouxe consigo uma força que poucas pessoas carregam tão jovem: a capacidade de enfrentar os próprios desafios sem recuar.\n\n'
     'Responsável e independente desde cedo, ela construiu seu caminho com as próprias mãos — e foi no <strong>Direito</strong> que encontrou sua vocação. A paixão pelo <strong>Direito Civil</strong>, especialmente pelo Direito de Família, não é apenas uma escolha acadêmica: é um reflexo de quem ela é — alguém que acredita nas relações humanas e na justiça como pilares da vida.\n\n'
     'Cinco anos depois, o diploma não é apenas um papel. É o símbolo de cada madrugada estudada, de cada obstáculo superado, e da certeza de que o esforço sempre tem um destino.'),
    ('agradecimento_frase',
     '"Nenhuma conquista se constrói sozinha. Este diploma carrega o nome de todos que acreditaram em mim quando eu mais precisei — e de alguns que nunca deixaram de estar ao meu lado."'),
    ('agradecimento_homenageados',
     'Meu Pai\nMinha Avó\nMeu Namorado\nMeu Melhor Colega\nMeus Professores\nToda a Família'),
    ('envio_descricao',
     'Tem uma memória especial com ela? Compartilhe aqui e faça parte desta galeria!'),
]

for secao, conteudo in textos:
    obj, criado = TextoSite.objects.get_or_create(secao=secao, defaults={'conteudo': conteudo})
    status = '✅ Criado' if criado else '⏭️  Já existe'
    print(f"  {status}: {secao}")

print("\nPopulando eventos...")
eventos = [
    {
        'tipo': 'missa',
        'nome_local': 'Paróquia Imaculada Conceição (Igreja dos Capuchinhos)',
        'endereco': 'Rua General Sampaio, 161 A\nBairro Rio Branco\nCaxias do Sul - RS, 95097-970',
        'data': date(2026, 7, 30),
        'horario': time(19, 30),
        'link_maps': 'https://maps.google.com/?q=Rua+General+Sampaio+161+Rio+Branco+Caxias+do+Sul',
    },
    {
        'tipo': 'colacao',
        'nome_local': 'Vila Poliesportiva da Universidade de Caxias do Sul',
        'endereco': 'R. Francisco Getúlio Vargas\nPetrópolis\nCaxias do Sul - RS, 95070-560',
        'data': date(2026, 7, 31),
        'horario': time(18, 0),
        'link_maps': 'https://maps.google.com/?q=Vila+Poliesportiva+UCS+Caxias+do+Sul',
    },
    {
        'tipo': 'almoco',
        'nome_local': 'Sítio Vovô Sady Costamilan',
        'endereco': 'Casarão Costamilan\nComunidade Nossa Senhora de Loreto\nSegunda Légua - Caxias do Sul',
        'data': date(2026, 8, 2),
        'horario': time(12, 0),
        'link_maps': 'https://maps.google.com/?q=Comunidade+Nossa+Senhora+de+Loreto+Caxias+do+Sul',
    },
]

for ev in eventos:
    obj, criado = Evento.objects.get_or_create(tipo=ev['tipo'], defaults=ev)
    status = '✅ Criado' if criado else '⏭️  Já existe'
    print(f"  {status}: {ev['tipo']}")

print("\n✨ Dados iniciais inseridos com sucesso!")
print("\nPróximo passo: crie o superusuário com:")
print("  python manage.py createsuperuser")
