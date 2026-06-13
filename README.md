# django-api

Basic Django API project scaffold.

![CI](https://github.com/ab-hakim-ayman/django-api/actions/workflows/ci.yml/badge.svg)

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
make ci
```

`make ci` runs the same SQA gate used in GitHub Actions.

## Environment Variables

Copy `.env.example` values into your shell or a local env file before production-grade setup.

## Task API

- `GET /api/tasks/` list tasks
- `POST /api/tasks/` create task
- `GET /api/tasks/<id>/` retrieve task
- `PUT/PATCH /api/tasks/<id>/` update task
- `DELETE /api/tasks/<id>/` delete task

## SQA

- Pull requests to `dev` and `main` run automated CI
- CI checks: Ruff, pytest, coverage threshold, Django system check
- Coverage report is exported as `coverage.xml`

## DevSecOps

- Run `make security` for static analysis, dependency audit, and Django deploy checks
- Production should set a unique `DJANGO_SECRET_KEY` and turn secure cookie/SSL flags on
- Security workflow runs Bandit, `pip-audit`, and Django `check --deploy`
