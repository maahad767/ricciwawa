web: gunicorn core.wsgi
worker: celery -A core worker --loglevel=info
release: python manage.py migrate