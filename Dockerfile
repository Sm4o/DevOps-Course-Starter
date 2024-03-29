FROM python:3.7-buster as base

WORKDIR /srv
#Update the system and install additional package
RUN apt-get update && apt-get install -y curl wget
COPY poetry.toml poetry.lock pyproject.toml /srv/
RUN pip install poetry
COPY todo_app /srv/todo_app
EXPOSE 5000

FROM base as production
ENV FLASK_ENV=production
COPY entrypoint.sh .
RUN poetry config virtualenvs.create false --local \
  && poetry install \ 
  && chmod +x ./entrypoint.sh
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh

FROM base as development
ENV FLASK_ENV=development
RUN poetry install
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000

FROM base as test
RUN apt-get install -y firefox-esr
RUN poetry install

# Install the latest version of Geckodriver:
RUN BASE_URL=https://github.com/mozilla/geckodriver/releases/download \
  && VERSION=$(curl -sL \
    https://api.github.com/repos/mozilla/geckodriver/releases/latest | \
    grep tag_name | cut -d '"' -f 4) \
  && curl -sL "$BASE_URL/$VERSION/geckodriver-$VERSION-linux64.tar.gz" | \
    tar -xz -C /usr/bin
ENV MOZ_HEADLESS=1
EXPOSE 4444
COPY . /srv
# ENTRYPOINT poetry run ptw --poll
ENTRYPOINT ["poetry", "run", "pytest"] 