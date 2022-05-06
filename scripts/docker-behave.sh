source .env
docker compose build todo-app-test
docker compose run -e TRELLO_TOKEN=$TRELLO_TOKEN -e TRELLO_KEY=$TRELLO_KEY -e SECRET_KEY=$SECRET_KEY -e TRELLO_ORGANIZATION=$TRELLO_ORGANIZATION todo-app-test poetry run behave