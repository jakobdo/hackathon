find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate

DJANGO_SUPERUSER_USERNAME=system \
DJANGO_SUPERUSER_EMAIL=j@kob.dk \
DJANGO_SUPERUSER_PASSWORD=Abc12345 \
python manage.py createsuperuser --noinput
