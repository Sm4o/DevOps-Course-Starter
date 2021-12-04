#!/bin/bash
set -e

# Get the latest image from Docker Hub (built by your CI pipeline) 
docker pull sm4o/todo.app:latest
# Tag it for Heroku
docker tag sm4o/todo.app:latest registry.heroku.com/"${APP_NAME}"/web
# Push it to Heroku registry
docker push registry.heroku.com/"${APP_NAME}"/web

# Release
heroku container:release web -a "${APP_NAME}"