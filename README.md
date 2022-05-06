# DevOps Apprenticeship: Project Exercise

## With docker 
### Setup 
run `scripts/generate_env.sh` to generate a .env file.

### Running the app
run either 
1. `docker compose up -d todo-app` to run the app in production mode on port 8080
1. `docker compose up -d todo-app-dev` to run in development mode on port 5000.

## Without docker
### Setup
run `source scripts/setup-apt.sh` or `source scripts/setup-yum.sh` depending on your package manager. 
If you use another package manager, check the scripts for dependencies needed.


You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

### Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Running the tests
With docker:
    First run `docker compose build todo-app-test`
    run `scripts/docker-tests.sh` to run unit and integration tests
    run `scripts/docker-behave.sh` to run e2e tests (requires .env file with valid Trello information)
Without docker:
    Requirements:
    - e2e tests require geckodriver and Firefox installed and in PATH,
        as well as valid Trello credentials set in .env
    How to run:
    - unit tests: poetry run pytest tests/unit
    - integration tests: poetry run pytest tests/integration
    - e2e tests: poetry run behave


## Running on a remote host using ansible
Steps:
Run `poetry run python scripts/generate_env.py` and enter values for environment variables needed on the remote host (first time only)
Run `scripts/deploy.sh`