#!/bin/bash
set -e
# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=$DB_PASSWORD pg_isready -h db -U $DB_USER -p 5432; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - continuing..."
# poetry install

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Running Django migrations..."
poetry run python manage.py migrate

echo "Starting Django server..."
poetry run python manage.py runserver 0.0.0.0:8000
