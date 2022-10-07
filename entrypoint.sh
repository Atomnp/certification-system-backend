python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

if [ "$PRODUCTION" == "true" ]
then
    gunicorn certification_system.wsgi:application --bind 0.0.0.0:8000 --reload
else
    python manage.py runserver 0.0.0.0:8000   
fi