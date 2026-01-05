#!/usr/bin/env sh
set -e

# If DB is postgres, wait for it to accept TCP connections
if [ "${DB_ENGINE:-}" = "postgres" ] || [ "${DB_ENGINE:-}" = "postgresql" ] || [ -n "${POSTGRES_DB:-}" ]; then
  echo "Waiting for database at ${DB_HOST:-db}:${DB_PORT:-5432} ..."
  python - <<'PY'
import os, time, socket, sys

host = os.getenv("DB_HOST", "db")
port = int(os.getenv("DB_PORT", "5432"))

for i in range(60):
    try:
        with socket.create_connection((host, port), timeout=2):
            print("Database is up")
            sys.exit(0)
    except OSError:
        time.sleep(1)

print("Database did not become ready in time", file=sys.stderr)
sys.exit(1)
PY
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Starting server..."
if [ "${GUNICORN:-1}" = "1" ]; then
  exec gunicorn exchange.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${WEB_CONCURRENCY:-3} \
    --timeout ${GUNICORN_TIMEOUT:-120}
else
  exec python manage.py runserver 0.0.0.0:8000
fi
