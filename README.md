# Microservice Template (Django + PostgreSQL + Nginx)

This repository provides a minimal Django project that can act as a template
for any microservice. It ships with PostgreSQL for storage and exposes the API
through Nginx.

## Quick start

1. Copy `.env.example` to `.env` and adjust the values if needed.
2. Start the stack with Docker Compose (Nginx listens on port `80`):

   ```bash
   docker compose up -d --build
   ```

The application will be available via Nginx on `http://localhost/`.


docker compose exec web python manage.py makemigrations api
docker compose exec web python manage.py migrate