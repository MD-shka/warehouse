#!/bin/bash
set -e

while ! nc -z db 5432; do
  sleep 1
done

if poetry run alembic revision --autogenerate -m "Initial migration" 2>/dev/null; then
  poetry run alembic upgrade head >/dev/null 2>&1
fi

exec "$@"
