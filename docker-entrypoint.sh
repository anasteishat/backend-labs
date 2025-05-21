#!/bin/bash
set -e

wait_for_db() {
    echo "Waiting for database..."
    for i in {1..10}; do
        if python -c "import psycopg2; psycopg2.connect('dbname=${POSTGRES_DB} user=${POSTGRES_USER} password=${POSTGRES_PASSWORD} host=${POSTGRES_HOST} port=${POSTGRES_PORT}')" >/dev/null 2>&1; then
            echo "Database is ready!"
            return 0
        fi
        echo "Database not ready yet... waiting 1 second"
        sleep 1
    done
    echo "Database connection failed after 10 seconds"
    return 1
}

wait_for_db

echo "Running database migrations..."
rm -rf migrations/
PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -p ${POSTGRES_PORT} -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "DELETE FROM alembic_version IF EXISTS;"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

echo "Starting application..."
exec flask run --host=0.0.0.0 --port=5000 