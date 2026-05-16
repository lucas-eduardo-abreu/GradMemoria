# GradMemoria

Memorial website for the 2026 Law School graduation of Micaelle Menezes Moreira —
UCS (Universidade de Caxias do Sul). All content is managed through the Django admin
panel; no code changes needed to update text, photos, or events.

## Stack

- Python 3.12 · Django 5.1 · Django Jazzmin · Cloudinary · PostgreSQL · Render

## Features

- **Gallery** — photo gallery with ordering, highlight flag, and Cloudinary storage
- **Guest photos** — visitors submit photos via the public site; an admin moderation
  workflow approves them before publication
- **Events** — date, time, venue, and Google Maps link for each graduation event
  (mass, graduation ceremony, reception)
- **Editable content** — all text sections (hero, history, acknowledgements) managed
  through the admin without code changes
- **Admin theme** — Jazzmin with a custom dark gold/burgundy skin

## Running locally

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python seed.py
python manage.py createsuperuser
python manage.py runserver
```

Public site at `http://localhost:8000`. Admin at `/admin/`.

## Deploy

Configured for Render via `render.yaml`. The build command runs `collectstatic`,
`migrate`, and `seed.py` automatically on every deploy.

Required env vars: `SECRET_KEY`, `DATABASE_URL`. Cloudinary credentials
(`CLOUDINARY_URL`) are needed for image uploads in production.
