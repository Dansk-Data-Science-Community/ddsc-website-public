.PHONY: help test test-unit test-api test-coverage test-watch lint format clean run migrate

help:
@echo "DDSC Makefile targets:"
@echo "  make test           - Run all tests"
@echo "  make test-unit      - Run unit tests only"
@echo "  make test-api       - Run API tests only"
@echo "  make test-coverage  - Run tests with coverage"
@echo "  make test-watch     - Run tests in watch mode"
@echo "  make lint           - Run linting"
@echo "  make format         - Format code"
@echo "  make migrate        - Run migrations"
@echo "  make run            - Run dev server"
@echo "  make clean          - Clean build artifacts"

test:
cd ddsc_web && pytest -v

test-unit:
cd ddsc_web && pytest -v -m unit

test-api:
cd ddsc_web && pytest -v -m api

test-coverage:
cd ddsc_web && pytest --cov --cov-report=html --cov-report=term-missing

test-watch:
cd ddsc_web && pytest -v -x -s --tb=short

lint:
flake8 ddsc_web --max-line-length=120
black --check ddsc_web
isort --check-only ddsc_web

format:
black ddsc_web
isort ddsc_web

migrate:
cd ddsc_web && python manage.py migrate

run:
cd ddsc_web && python manage.py runserver

clean:
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name '*.pyc' -delete
find . -type d -name '.pytest_cache' -exec rm -rf {} +
rm -rf htmlcov coverage.xml .coverage
