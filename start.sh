#!/usr/bin/env sh

echo "Starting the web server................."
# python manage.py makemigrations
# python manage.py migrate
# python manage.py collectstatic --noinput
# python manage.py add_all_data
# python manage.py runserver 0.0.0.0:$PORT
gunicorn project.wsgi --bind 0.0.0.0:$PORT --workers 2 --worker-class gthread --threads 3 --worker-connections 1000 --timeout 30 --keep-alive 5 --access-logfile - --log-file - --log-level info --capture-output