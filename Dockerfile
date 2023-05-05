# Указываем базовый образ
FROM python:3.11

# Устанавливаем переменную окружения PYTHONUNBUFFERED, чтобы Python вывел все выводы сразу, без буферизации
ENV PYTHONUNBUFFERED 1

# Создаем рабочую директорию внутри Docker контейнера
RUN mkdir /code
WORKDIR /code

# Копируем зависимости проекта в Docker контейнер
COPY requirements.txt /code/

# Устанавливаем зависимости проекта в Docker контейнер
RUN pip install -r requirements.txt

# Копируем код проекта в Docker контейнер
COPY . /code/

# Устанавливаем PostgreSQL в качестве базы данных
RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib

# Запускаем PostgreSQL и создаем базу данных
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE DATABASE lunch_place;" && \
    psql --command "GRANT ALL PRIVILEGES ON DATABASE lunch_place TO postgres;" && \
    psql --command "ALTER USER postgres PASSWORD 'postgres';"

USER root

# Запускаем приложение Django
RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py runscript setup

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
