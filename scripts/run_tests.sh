docker build --target test --tag todo.app:test .
docker run --env-file .env.test todo.app:test tests
docker run -e SECRET_KEY -e DATABASE_NAME -e DB_CONNECTION todo.app:test tests_e2e