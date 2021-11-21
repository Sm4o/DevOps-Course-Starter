docker build --target production --tag sm4o/todo.app:latest .
docker build --target production --tag sm4o/todo.app:$TRAVIS_COMMIT .
docker push sm4o/todo.app:latest
docker push sm4o/todo.app:$TRAVIS_COMMIT