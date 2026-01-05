#!/usr/bin/env bash
set -e
docker compose exec web python manage.py test -v 2
