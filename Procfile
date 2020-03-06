release: python manage.py migrate && python manage.py loaddata ./adventure/fixtures/all_chambers.json


web: gunicorn adv_project.wsgi:application --log-file -
