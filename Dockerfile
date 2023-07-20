FROM python:3.11.4

ENV PYTHONDONWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /code
RUN pip install --upgrade pip

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD ["python", "manage.py", "runserver"]
