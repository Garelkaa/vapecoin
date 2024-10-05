MANAGE = python manage.py
SOURCE = src
MAIN = vapecoin

PROJECT_DIR=$(shell pwd)
WSGI_PORT=8000
                                  
run:
	$(MANAGE) runserver 127.0.0.1:8000

gunicorn-run:
	gunicorn vapecoin.wsgi:application -b 0.0.0.0:8000 --reload

migrations:
	$(MANAGE) makemigrations --no-input
	$(MANAGE) migrate --no-input
	$(MANAGE) collectstatic --clear --noinput

	python fill_table.py
	gunicorn vapecoin.wsgi:application -b 0.0.0.0:8000 --reload

start-app:
	cd $(SOURCE) && python manage.py startapp $(app)

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

shell: # only after 'make extensions-install'
	$(MANAGE) shell_plus --print-sql


install:
	pip install -r requirements.txt

check:
	$(MANAGE) check

migrations-dry:
	$(MANAGE) makemigrations --dry-run
