from argparse import ArgumentError
import json
import re
from unittest.mock import MagicMock
import dotenv
import pytest

import requests
import todo_app.app
from todo_app.data.items_backend import Item, Status
from todo_app.data.trello.trello_items import STATUS_TO_LIST_NAME
import todo_app.data.trello.trello_request
from todo_app.app import create_app


@pytest.fixture
def test_client():
    dotenv.load_dotenv(".env.test", override=True)
    test_app = create_app()
    with test_app.test_client() as client:
        yield client


@pytest.fixture
def trello_backend(monkeypatch):
    monkeypatch.setattr(todo_app.app, "session", {"ItemBackend": "Trello"})


def request_mock(lists, cards):
    def request(method, url, params):
        assert method == "get"
        return_table = {
            "https://api.trello.com/1/boards/BOARD101112/lists": lists,
            "https://api.trello.com/1/boards/BOARD101112/cards": cards,
        }

        ret = return_table.get(url)
        if ret is None:
            match = re.match("https://api.trello.com/1/lists/(listid[0-9]+)/cards", url)
            if match:
                list_id = match.group(1)
                ret = [card for card in cards if card["idList"] == list_id]
            else:
                raise ArgumentError(f"Invalid URL {url}")
        mock_response = MagicMock()
        mock_response.json.return_value = ret
        return mock_response

    return request


@pytest.fixture
def mock_requests_default(monkeypatch):
    lists = [
        {"id": "listid123", "name": STATUS_TO_LIST_NAME[Status.TODO]},
        {"id": "listid456", "name": STATUS_TO_LIST_NAME[Status.DOING]},
        {"id": "listid789", "name": STATUS_TO_LIST_NAME[Status.DONE]},
    ]
    cards = [
        {"id": "cardid123", "name": "Test Card 1", "idList": "listid123"},
        {"id": "cardid123", "name": "Test Card 1", "idList": "listid123"},
    ]
    monkeypatch.setattr(requests, "request", request_mock(lists, cards))


def test_index(monkeypatch, trello_backend, test_client, mock_requests_default):
    response = test_client.get("/")
    assert response.status == "200 OK"
    response_as_str = str(response.data)
    assert "Current item storage method: Trello" in response_as_str
    assert "Test Card 1" in response_as_str
    assert "To do" in response_as_str
    assert "Doing" in response_as_str
    assert "Done" in response_as_str


def test_switch_backend(mock_requests_default, test_client):
    response = test_client.get("/")
    assert "Current item storage method: Session" in str(response.data)
    switch_response = test_client.post("/switchbackend")
    assert switch_response.status == "302 FOUND"
    response_after_switch = test_client.get(switch_response.headers["Location"])
    assert "Current item storage method: Trello" in str(response_after_switch.data)
    switch_back_response = test_client.post("/switchbackend")
    assert switch_back_response.status == "302 FOUND"
    response_after_switch_back = test_client.get(
        switch_back_response.headers["Location"]
    )
    assert "Current item storage method: Session" in str(
        response_after_switch_back.data
    )
