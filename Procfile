release: python3 manage.py migrate
web: gunicorn adv_project.wsgi:application --log-file -


python manage.py loaddata ./fixtures/all_chambers.json