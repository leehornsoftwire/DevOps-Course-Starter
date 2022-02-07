import logging
import os
from multiprocessing import Process

import dotenv
from behave import fixture, use_fixture
from behave.fixture import use_fixture_by_tag
from flask import Flask
from selenium import webdriver

from todo_app.app import create_app
from todo_app.data.trello.trello_items import TrelloItems
from todo_app.data.trello.trello_request import TrelloRequest


@fixture
def test_app(context):
    dotenv.load_dotenv(".env")
    os.environ[
        "WERKZEUG_RUN_MAIN"
    ] = "true"  # Trick flask into thinking we are restarting to suppress console output
    log = logging.getLogger("werkzeug")
    log.disabled = True
    test_app: Flask = create_app()
    process = Process(target=lambda: test_app.run(use_reloader=False, debug=False))
    process.start()
    yield test_app

    process.kill()


@fixture
def test_trello_board(context):
    dotenv.load_dotenv(".env")
    app_token = os.environ["TRELLO_TOKEN"]
    key = os.environ["TRELLO_KEY"]
    organization = os.environ["TRELLO_ORGANIZATION"]
    response = (
        TrelloRequest.new(app_token, key)
        .with_url("/boards")
        .with_params({"name": "TodoAppE2ETest", "idOrganization": organization})
        .post()
        .json()
    )
    board_id = response["id"]
    os.environ["TRELLO_BOARD"] = board_id
    context.add_cleanup(lambda: TrelloItems.load().delete_board())
    return board_id


@fixture
def firefox(context):
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    context.driver = driver

    yield driver

    driver.quit()


fixture_registry = {
    "fixture.test_trello_board": test_trello_board,
    "fixture.test_app": test_app,
    "fixture.firefox": firefox,
}


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)


def before_scenario(context, scenario):
    use_fixture(firefox, context)
