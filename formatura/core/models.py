from django.db import models
from django.utils import timezone


class FotoFormanda(models.Model):
    imagem = models.ImageField(upload_to='formanda/', verbose_name='Foto da formanda')
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Foto da formanda'
        verbose_name_plural = 'Foto da formanda'

    def __str__(self):
        return 'Foto principal'

    def save(self, *args, **kwargs):
        # garante que só existe um registro
        self.__class__.objects.exclude(pk=self.pk).delete()
        super().save(*args, **kwargs)


class TextoSite(models.Model):
    SECAO_CHOICES = [
        ('hero_titulo', 'Hero — Título principal'),
        ('hero_subtitulo', 'Hero — Subtítulo (curso/universidade)'),
        ('historia_titulo', 'História — Título da seção'),
        ('historia_corpo', 'História — Texto principal'),
        ('agradecimento_frase', 'Agradecimento — Frase/citação'),
        ('agradecimento_homenageados', 'Agradecimento — Homenageados (um por linha)'),
        ('envio_descricao', 'Envio de fotos — Descrição'),
    ]

    secao = models.CharField(
        max_length=60,
        choices=SECAO_CHOICES,
        unique=True,
        verbose_name='Seção',
    )
    conteudo = models.TextField(verbose_name='Conteúdo')
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Texto do site'
        verbose_name_plural = 'Textos do site'
        ordering = ['secao']

    def __str__(self):
        return self.get_secao_display()


class Evento(models.Model):
    TIPO_CHOICES = [
        ('missa', 'Missa'),
        ('colacao', 'Colação de Grau'),
        ('almoco', 'Almoço / Festa'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, unique=True, verbose_name='Tipo')
    nome_local = models.CharField(max_length=200, verbose_name='Nome do local')
    endereco = models.TextField(verbose_name='Endereço completo')
    data = models.DateField(verbose_name='Data')
    horario = models.TimeField(verbose_name='Horário')
    link_maps = models.URLField(blank=True, verbose_name='Link Google Maps')
    ativo = models.BooleanField(default=True, verbose_name='Exibir no site')

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data', 'horario']

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.data.strftime('%d/%m/%Y')} às {self.horario.strftime('%H:%M')}"


class FotoGaleria(models.Model):
    imagem = models.ImageField(upload_to='galeria/', verbose_name='Imagem')
    legenda = models.CharField(max_length=200, blank=True, verbose_name='Legenda (opcional)')
    ordem = models.PositiveIntegerField(default=0, verbose_name='Ordem de exibição')
    destaque = models.BooleanField(default=False, verbose_name='Foto destaque (maior)')
    ativa = models.BooleanField(default=True, verbose_name='Exibir na galeria')
    adicionada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto da galeria'
        verbose_name_plural = 'Fotos da galeria'
        ordering = ['ordem', '-adicionada_em']

    def __str__(self):
        return self.legenda or f"Foto #{self.pk}"


class FotoConvidado(models.Model):
    nome = models.CharField(max_length=120, verbose_name='Nome do remetente')
    relacionamento = models.CharField(max_length=120, blank=True, verbose_name='Relação com a Micaelle')
    mensagem = models.TextField(blank=True, verbose_name='Mensagem')
    imagem = models.ImageField(upload_to='convidados/', verbose_name='Foto')
    aprovada = models.BooleanField(default=False, verbose_name='Aprovada (publicar na galeria)')
    enviada_em = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Foto enviada por convidado'
        verbose_name_plural = 'Fotos enviadas por convidados'
        ordering = ['-enviada_em']

    def __str__(self):
        status = '✅ Aprovada' if self.aprovada else '⏳ Aguardando aprovação'
        return f"{self.nome} — {status}"
