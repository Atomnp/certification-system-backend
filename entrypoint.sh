python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

gunicorn certification_system.wsgi:application --bind 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000