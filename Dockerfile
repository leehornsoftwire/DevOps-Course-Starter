# Create a production image, with multi-stage builds used to reduce image size.
FROM python:3.9-slim-bullseye as poetry 
RUN apt-get update 
RUN apt-get -y install wget
RUN wget -O install-poetry.py https://install.python-poetry.org
RUN python install-poetry.py -y
ENV PATH="/root/.local/bin:$PATH"

FROM poetry as development
WORKDIR /opt/todoapp

ENV FLASK_APP=todo_app/app
ENV FLASK_ENV=development

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install

COPY scripts scripts

ENTRYPOINT ["/bin/bash", "-c",  "poetry run flask run --host 0.0.0.0"]

FROM poetry as build
COPY pyproject.toml /srv/todoapp/pyproject.toml
COPY scripts /srv/todoapp/scripts
COPY todo_app /srv/todoapp/todo_app
WORKDIR /srv/todoapp
RUN scripts/build.sh

FROM poetry as test 
RUN apt-get update
RUN apt-get -y install firefox-esr
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux32.tar.gz
RUN tar -xzf geckodriver-v0.31.0-linux32.tar.gz
RUN mv geckodriver /bin/geckodriver
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY todo_app todo_app
RUN poetry install
COPY tests tests
COPY features features
COPY .env.test .env.test

FROM python:3.9-slim-bullseye
ENV FLASK_ENV=production
RUN pip install waitress
COPY --from=build /srv/todoapp/dist/todo_app-0.1.0-py3-none-any.whl /opt/todoapp/todo_app-0.1.0-py3-none-any.whl
RUN pip install /opt/todoapp/todo_app-0.1.0-py3-none-any.whl

CMD ["waitress-serve", "--port=8080", "--call", "todo_app.app:create_app"]