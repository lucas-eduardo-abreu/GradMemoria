# ✦ GradMemoria

Site memorial para a formatura em Direito pela Universidade de Caxias do Sul (UCS), 2026.

---

## Estrutura do Projeto

```
formatura_micaelle/
├── formatura/          # Configurações Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/               # App principal
│   ├── models.py       # TextoSite, Evento, FotoGaleria, FotoConvidado
│   ├── admin.py        # Painel admin customizado (Jazzmin)
│   ├── views.py        # Home + API de envio de fotos
│   ├── urls.py
│   └── templates/core/home.html
├── static/
│   └── css/admin_custom.css   # Tema dourado/bordô no admin
├── seed.py             # Popula dados iniciais
├── render.yaml         # Deploy no Render
├── requirements.txt
└── .env.example
```

---

## Rodar Localmente

```bash
# 1. Clone e entre na pasta
cd formatura_micaelle

# 2. Crie o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o .env
cp .env.example .env
# Edite o .env com: SECRET_KEY=qualquer-string-longa, DEBUG=True

# 5. Crie o banco e popule dados iniciais
python manage.py migrate
python seed.py

# 6. Crie o superusuário (login do admin)
python manage.py createsuperuser

# 7. Rode o servidor
python manage.py runserver
```

Acesse:
- Site: http://localhost:8000/
- Admin: http://localhost:8000/admin/

---

## Deploy no Render

1. Faça push do projeto para um repositório GitHub
2. No Render, clique em **New > Blueprint**
3. Conecte o repositório — o `render.yaml` configura tudo automaticamente
4. Após o deploy, acesse `/admin` e crie o superusuário via **Shell** do Render:
   ```bash
   python manage.py createsuperuser
   ```

---

## O que a Micaelle pode editar no Admin (/admin)

| Seção | O que editar |
|---|---|
| **Textos do site** | Todos os textos: história, agradecimentos, descrições |
| **Eventos** | Data, horário, endereço e link do mapa de cada evento |
| **Fotos da galeria** | Adicionar, remover, reordenar fotos. Marcar como destaque |
| **Fotos de convidados** | Ver fotos enviadas e aprovar/rejeitar antes de publicar |

### Fluxo das fotos de convidados:
1. Convidado envia foto pelo site
2. Micaelle recebe no admin em **"Fotos enviadas por convidados"** com status **⏳ Pendente**
3. Ela visualiza a foto e clica para **aprovar**
4. A foto aparece automaticamente na galeria do site ✅

---

## Modelos do banco de dados

- **TextoSite** — textos editáveis por seção (história, agradecimentos, etc.)
- **Evento** — missa, colação e almoço com data/horário/endereço
- **FotoGaleria** — fotos da Micaelle na galeria principal (com ordem e destaque)
- **FotoConvidado** — fotos enviadas por convidados (com moderação)

---

## Tecnologias

- Django 5.0
- Django Jazzmin (admin customizado)
- WhiteNoise (servir arquivos estáticos)
- PostgreSQL (produção) / SQLite (desenvolvimento)
- Gunicorn (servidor WSGI)
- Render (hospedagem)
