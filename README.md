# fisdom

mysql: sudo apt-get install mysql-server
rabbitmq: sudo apt-get install rabbitmq-server

celery: celery -A fisdom worker -Q celery --loglevel=info

cd fisdom python=python3.8
pipenv shell
python manage.py migrate
python manage.py collectstatic
python manage.py runserver

