docker build --target test --tag todo.app:test .
docker run --env-file .env.test todo.app:test tests
docker run --env BOARD_ID --env APP_KEY --env TOKEN todo.app:test tests_e2e