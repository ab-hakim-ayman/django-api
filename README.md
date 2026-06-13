# django-api

Basic Django API project scaffold.

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

## Development Workflow

- Main stable branch: `main`
- Active development branch: `dev`
- Install hooks: `. .venv/bin/activate && pre-commit install`

## Quality Commands

```bash
make check
make lint
make format
make test
make pre-commit
```

## Environment Variables

Copy `.env.example` values into your shell or a local env file before production-grade setup.

## Task API

- `GET /api/tasks/` list tasks
- `POST /api/tasks/` create task
- `GET /api/tasks/<id>/` retrieve task
- `PUT/PATCH /api/tasks/<id>/` update task
- `DELETE /api/tasks/<id>/` delete task
