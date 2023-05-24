#!/usr/bin/env sh

echo "Starting the web server................."
echo "Running release comands..."
# python manage.py makemigrations
# python manage.py migrate
python manage.py collectstatic --noinput
# python manage.py add_all_data
python manage.py runserver 0.0.0.0:$PORT