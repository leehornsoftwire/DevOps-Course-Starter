#!/bin/bash -e 
if [[ ! -f .env ]]; then
	echo "No dotenv file found!"
	exit 1
fi

export $(cat .env|xargs)
venv/bin/waitress-serve --port=8080 --call "todo_app.app:create_app"
