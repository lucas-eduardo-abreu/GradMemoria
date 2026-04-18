from django.contrib import admin
from django.utils.html import format_html
from .models import TextoSite, Evento, FotoGaleria, FotoConvidado, FotoFormanda


@admin.register(FotoFormanda)
class FotoFormandaAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'atualizada_em']
    readonly_fields = ['thumb_grande', 'atualizada_em']

    def thumb(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="width:55px;height:70px;object-fit:cover;border-radius:4px;'
                'border:2px solid #C9A84C;" />',
                obj.imagem.url
            )
        return '—'
    thumb.short_description = 'Foto'

    def thumb_grande(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-width:300px;max-height:380px;object-fit:cover;'
                'border-radius:8px;border:2px solid #C9A84C;" />',
                obj.imagem.url
            )
        return '—'
    thumb_grande.short_description = 'Pré-visualização'

    fieldsets = (
        ('Foto principal do hero', {
            'description': 'Esta foto aparece na seção principal do site. Proporção ideal: retrato (3×4).',
            'fields': ('imagem', 'thumb_grande', 'atualizada_em'),
        }),
    )


@admin.register(TextoSite)
class TextoSiteAdmin(admin.ModelAdmin):
    list_display = ['secao_display', 'preview_conteudo', 'atualizado_em']
    list_display_links = ['secao_display']
    readonly_fields = ['atualizado_em']

    def secao_display(self, obj):
        return obj.get_secao_display()
    secao_display.short_description = 'Seção'

    def preview_conteudo(self, obj):
        texto = obj.conteudo[:80] + '…' if len(obj.conteudo) > 80 else obj.conteudo
        return texto
    preview_conteudo.short_description = 'Prévia'

    fieldsets = (
        (None, {
            'fields': ('secao', 'conteudo', 'atualizado_em'),
            'description': 'Edite os textos que aparecem no site. As alterações ficam visíveis imediatamente.',
        }),
    )


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['tipo_badge', 'nome_local', 'data_formatada', 'horario_formatado', 'ativo']
    list_display_links = ['nome_local']
    list_editable = ['ativo']
    list_filter = ['ativo', 'tipo']

    def tipo_badge(self, obj):
        cores = {
            'missa': '#8B2035',
            'colacao': '#C9A84C',
            'almoco': '#3D0A15',
        }
        icones = {'missa': '⛪', 'colacao': '🎓', 'almoco': '🍽️'}
        cor = cores.get(obj.tipo, '#888')
        icone = icones.get(obj.tipo, '')
        return format_html(
            '<span style="background:{};color:#F5EDD6;padding:3px 10px;border-radius:4px;font-size:12px;font-weight:600">'
            '{} {}</span>',
            cor, icone, obj.get_tipo_display()
        )
    tipo_badge.short_description = 'Tipo'

    def data_formatada(self, obj):
        return obj.data.strftime('%d/%m/%Y')
    data_formatada.short_description = 'Data'

    def horario_formatado(self, obj):
        return obj.horario.strftime('%H:%M')
    horario_formatado.short_description = 'Horário'

    fieldsets = (
        ('Identificação', {'fields': ('tipo', 'ativo')}),
        ('Local', {'fields': ('nome_local', 'endereco', 'link_maps')}),
        ('Data e horário', {'fields': ('data', 'horario')}),
    )


@admin.register(FotoGaleria)
class FotoGaleriaAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'legenda_display', 'ordem', 'destaque', 'destaque_badge', 'ativa', 'adicionada_em']
    list_display_links = ['thumb', 'legenda_display']
    list_editable = ['ordem', 'ativa', 'destaque']
    list_filter = ['ativa', 'destaque']
    search_fields = ['legenda']

    def thumb(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:4px;'
                'border:2px solid #C9A84C;" />',
                obj.imagem.url
            )
        return '—'
    thumb.short_description = 'Foto'

    def legenda_display(self, obj):
        return obj.legenda or f'Foto #{obj.pk}'
    legenda_display.short_description = 'Legenda'

    def destaque_badge(self, obj):
        if obj.destaque:
            return format_html(
                '<span style="background:#C9A84C;color:#3D0A15;padding:2px 8px;'
                'border-radius:4px;font-size:11px;font-weight:700">★ DESTAQUE</span>'
            )
        return '—'
    destaque_badge.short_description = 'Destaque'

    fieldsets = (
        ('Imagem', {'fields': ('imagem', 'legenda')}),
        ('Configurações de exibição', {'fields': ('ordem', 'destaque', 'ativa')}),
    )


@admin.register(FotoConvidado)
class FotoConvidadoAdmin(admin.ModelAdmin):
    list_display = ['thumb', 'nome', 'relacionamento', 'aprovada', 'aprovada_badge', 'enviada_em']
    list_display_links = ['thumb', 'nome']
    list_editable = ['aprovada']
    list_filter = ['aprovada']
    search_fields = ['nome', 'relacionamento', 'mensagem']
    readonly_fields = ['thumb_grande', 'nome', 'relacionamento', 'mensagem', 'enviada_em']
    actions = ['aprovar_selecionadas', 'reprovar_selecionadas']

    def thumb(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="width:55px;height:55px;object-fit:cover;border-radius:4px;'
                'border:2px solid {};"/>',
                obj.imagem.url,
                '#C9A84C' if obj.aprovada else '#8B2035'
            )
        return '—'
    thumb.short_description = 'Foto'

    def thumb_grande(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-width:400px;max-height:400px;object-fit:contain;'
                'border-radius:8px;border:2px solid #C9A84C;" />',
                obj.imagem.url
            )
        return '—'
    thumb_grande.short_description = 'Pré-visualização'

    def aprovada_badge(self, obj):
        if obj.aprovada:
            return format_html(
                '<span style="background:#1a6b35;color:#d4f5e2;padding:3px 10px;'
                'border-radius:4px;font-size:12px">✅ Aprovada</span>'
            )
        return format_html(
            '<span style="background:#6b1a1a;color:#f5d4d4;padding:3px 10px;'
            'border-radius:4px;font-size:12px">⏳ Pendente</span>'
        )
    aprovada_badge.short_description = 'Status'

    def aprovar_selecionadas(self, request, queryset):
        count = queryset.update(aprovada=True)
        self.message_user(request, f'{count} foto(s) aprovada(s) com sucesso! ✅')
    aprovar_selecionadas.short_description = 'Aprovar fotos selecionadas'

    def reprovar_selecionadas(self, request, queryset):
        count = queryset.update(aprovada=False)
        self.message_user(request, f'{count} foto(s) movida(s) de volta para pendente.')
    reprovar_selecionadas.short_description = 'Mover para pendente'

    fieldsets = (
        ('Remetente', {'fields': ('nome', 'relacionamento', 'mensagem')}),
        ('Foto', {'fields': ('thumb_grande', 'imagem')}),
        ('Moderação', {'fields': ('aprovada', 'enviada_em')}),
    )
