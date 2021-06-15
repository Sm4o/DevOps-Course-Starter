FROM python:3.7-buster as base

WORKDIR /srv
COPY poetry.toml poetry.lock pyproject.toml /srv
RUN pip install poetry && poetry install
COPY todo_app /srv/todo_app
EXPOSE 5000

FROM base as production

ENV FLASK_ENV=production
ENTRYPOINT poetry run gunicorn --bind 0.0.0.0:5000 'todo_app.app:create_app()' 

FROM base as development

ENV FLASK_ENV=development
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000