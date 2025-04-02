#!/bin/sh

set -e # Exit the script immediately if any command fails

python manage.py wait_for_db # Ensures the database is ready before proceeding
python manage.py collectstatic --noinput # gathers all static files into STATIC_ROOT (used in production).
python manage.py migrate # Applies database migrations

# Starts the application using uWSGI (a production WSGI server) instead of the Django development server.
# uWSGI is faster and more efficient than Django’s built-in development server.
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi