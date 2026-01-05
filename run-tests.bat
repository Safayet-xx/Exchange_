@echo off
REM Run Django tests inside the web container
docker compose exec web python manage.py test -v 2
