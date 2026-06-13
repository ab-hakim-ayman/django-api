.PHONY: setup dev migrate lint format test check pre-commit ci security collectstatic run-prod docker-build release-check

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements-dev.txt

dev:
	. .venv/bin/activate && python manage.py runserver

migrate:
	. .venv/bin/activate && python manage.py migrate

collectstatic:
	. .venv/bin/activate && python manage.py collectstatic --noinput

lint:
	. .venv/bin/activate && ruff check .

format:
	. .venv/bin/activate && ruff format .

test:
	. .venv/bin/activate && pytest

check:
	. .venv/bin/activate && python manage.py check

pre-commit:
	. .venv/bin/activate && pre-commit run --all-files

ci:
	. .venv/bin/activate && ruff check .
	. .venv/bin/activate && pytest
	. .venv/bin/activate && python manage.py check

security:
	. .venv/bin/activate && bandit -r . -c pyproject.toml
	. .venv/bin/activate && pip-audit -r requirements.txt
	. .venv/bin/activate && env \
		DJANGO_SECRET_KEY=production-like-local-secret-key-with-strong-entropy-123456 \
		DJANGO_DEBUG=False \
		DJANGO_ALLOWED_HOSTS=api.example.com \
		DJANGO_CSRF_TRUSTED_ORIGINS=https://api.example.com \
		DJANGO_SECURE_HSTS_SECONDS=3600 \
		DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True \
		DJANGO_SECURE_HSTS_PRELOAD=True \
		DJANGO_SECURE_SSL_REDIRECT=True \
		DJANGO_SESSION_COOKIE_SECURE=True \
		DJANGO_CSRF_COOKIE_SECURE=True \
		python manage.py check --deploy --fail-level WARNING

run-prod:
	. .venv/bin/activate && gunicorn django_api.wsgi:application --bind 0.0.0.0:8000

docker-build:
	docker build -t django-api:latest .

release-check:
	$(MAKE) ci
	$(MAKE) security
