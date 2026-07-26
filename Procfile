web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn roselle_project.wsgi -b 0.0.0.0:$PORT
