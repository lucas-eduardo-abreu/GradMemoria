# GradMemoria

Site memorial para a formatura em Direito de Micaelle Menezes Moreira pela Universidade de Caxias do Sul — UCS, turma 2026.

Permite gerenciar textos, eventos, galeria de fotos e receber fotos enviadas por convidados, tudo via painel administrativo.

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Framework | Django 5.1 |
| Admin | Django Jazzmin 3.0 |
| Estáticos | WhiteNoise |
| Banco (dev) | SQLite |
| Banco (prod) | PostgreSQL |
| Servidor WSGI | Gunicorn |
| Hospedagem | Render |

---

## Estrutura

```
GradMemoria/
├── formatura/               # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── formatura/core/          # App principal
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   ├── urls.py
│   └── templates/core/home.html
├── static/
│   └── css/admin_custom.css
├── manage.py
├── seed.py
├── render.yaml
├── requirements.txt
└── .env.example
```

---

## Rodando localmente

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd GradMemoria

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env: defina SECRET_KEY e DEBUG=True

# 5. Aplique as migrations e popule os dados iniciais
python manage.py migrate
python seed.py

# 6. Crie o superusuário para acessar o admin
python manage.py createsuperuser

# 7. Inicie o servidor
python manage.py runserver
```

| URL | Descrição |
|---|---|
| http://localhost:8000/ | Site público |
| http://localhost:8000/admin/ | Painel administrativo |

---

## Deploy no Render

1. Faça push do projeto para um repositório GitHub
2. No Render, acesse **New → Blueprint** e conecte o repositório
3. O `render.yaml` configura automaticamente o serviço web e o banco PostgreSQL
4. Após o primeiro deploy, crie o superusuário via **Shell** do Render:
   ```bash
   python manage.py createsuperuser
   ```

O build executa automaticamente `collectstatic`, `migrate` e `seed.py`.

---

## Painel administrativo

| Seção | Função |
|---|---|
| **Foto da formanda** | Foto principal exibida no hero do site |
| **Textos do site** | Todos os textos editáveis: história, agradecimentos, descrições |
| **Eventos** | Data, horário, local e link do mapa de cada evento |
| **Fotos da galeria** | Adicionar, remover e reordenar fotos; marcar destaque |
| **Fotos de convidados** | Moderar fotos enviadas pelos convidados antes de publicar |

**Fluxo de moderação de fotos:**

1. Convidado envia foto pelo site
2. A foto aparece no admin com status **Pendente**
3. Após aprovação, é publicada automaticamente na galeria

---

## Modelos

| Modelo | Descrição |
|---|---|
| `FotoFormanda` | Foto principal da formanda (hero) |
| `TextoSite` | Textos editáveis por seção |
| `Evento` | Missa, colação e almoço — data, horário, endereço |
| `FotoGaleria` | Fotos da galeria principal com ordem e destaque |
| `FotoConvidado` | Fotos enviadas por convidados com moderação |
