.PHONY: setup dev migrate lint format test check pre-commit

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements-dev.txt

dev:
	. .venv/bin/activate && python manage.py runserver

migrate:
	. .venv/bin/activate && python manage.py migrate

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
