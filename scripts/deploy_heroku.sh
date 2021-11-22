#!/bin/bash
set -e

# Get the latest image from Docker Hub (built by your CI pipeline) 
docker pull sm4o/todo.app:latest
# Tag it for Heroku
docker tag sm4o/todo.app:latest registry.heroku.com/todo-app-corndel/web
# Push it to Heroku registry
docker push registry.heroku.com/todo-app-corndel/web

# Release
heroku container:release web