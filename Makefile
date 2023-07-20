install:
	pip install -r requirements.txt
	pip install --upgrade pip

run:
	python manage.py runserver

test:
	python manage.py test