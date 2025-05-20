#!/bin/bash
set -e

wait_for_db() {
    echo "Waiting for database..."
    for i in {1..12}; do
        if python -c "import psycopg2; psycopg2.connect('dbname=${POSTGRES_DB} user=${POSTGRES_USER} password=${POSTGRES_PASSWORD} host=${POSTGRES_HOST} port=${POSTGRES_PORT}')" >/dev/null 2>&1; then
            echo "Database is ready!"
            return 0
        fi
        echo "Database not ready yet... waiting 5 seconds"
        sleep 5
    done
    echo "Database connection failed after 60 seconds"
    return 1
}

wait_for_db

echo "Running database migrations..."
flask db upgrade

echo "Starting application..."
exec flask run --host=0.0.0.0 --port=5000 