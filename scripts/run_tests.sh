docker build --target test --tag todo.app:test .
docker run --env-file .env.test todo.app:test tests
docker run --env MONGODB_CONNECTION --env DATABASE_NAME --env SECRET_KEY --env DATABASE_NAME todo.app:test tests_e2e