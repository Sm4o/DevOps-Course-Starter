#!/bin/bash
set -e

docker build --target production --tag sm4o/todo.app:latest --tag sm4o/todo.app:$TRAVIS_COMMIT .
docker push sm4o/todo.app --all-tags

# Tag it for Heroku
docker tag sm4o/todo.app:latest registry.heroku.com/"${APP_NAME}"/web
# Push it to Heroku registry
docker push registry.heroku.com/"${APP_NAME}"/web

# Release
heroku container:release web -a "${APP_NAME}"