from typing import Dict
import pytest
from todo_app.data.items_backend import Item, Status
from todo_app.data.trello.trello_items import (
    LIST_NAME_TO_STATUS,
    STATUS_TO_LIST_NAME,
    TrelloItems,
    TrelloList,
    TrelloRequest,
    items_from_json,
    trello_lists_from_json,
)


def test_load_environment(monkeypatch):
    monkeypatch.setenv("TRELLO_TOKEN", "APPTOKEN123")
    monkeypatch.setenv("TRELLO_KEY", "APPKEY456")
    monkeypatch.setenv("TRELLO_BOARD", "TRELLOBOARD789")
    assert TrelloItems.load_environment() == TrelloItems(
        "APPTOKEN123", "APPKEY456", "TRELLOBOARD789"
    )


@pytest.mark.parametrize(
    "relative_url,expected_url_without_board, expected_url_with_board",
    [
        pytest.param(
            "cards",
            "https://api.trello.com/1/cards",
            "https://api.trello.com/1/boards/TRELLOBOARD789/cards",
            id="relative url",
        ),
        pytest.param(
            "",
            "https://api.trello.com/1/",
            "https://api.trello.com/1/boards/TRELLOBOARD789/",
            id="base url",
        ),
    ],
)
def test_get_trello_request(
    relative_url, expected_url_without_board, expected_url_with_board
):
    trello_items = TrelloItems("APPTOKEN123", "APPKEY456", "TRELLOBOARD789")
    expected_without_board = TrelloRequest(
        {"token": "APPTOKEN123", "key": "APPKEY456"}, expected_url_without_board
    )
    expected_with_board = TrelloRequest(
        {"token": "APPTOKEN123", "key": "APPKEY456"}, expected_url_with_board
    )
    assert trello_items.get_trello_request(relative_url) == expected_without_board
    assert (
        trello_items.get_trello_request_for_board(relative_url) == expected_with_board
    )


@pytest.fixture
def no_tokens_trello_items():
    return TrelloItems(None, None, None)


@pytest.mark.parametrize(
    "lists",
    [
        pytest.param(
            {
                "111": TrelloList(STATUS_TO_LIST_NAME[Status.TODO]),
                "112": TrelloList(STATUS_TO_LIST_NAME[Status.DONE]),
            }
        )
    ],
)
@pytest.mark.parametrize(
    "as_json,expected",
    [
        pytest.param(
            [{"id": "1234", "idList": "111", "name": "Barry"}],
            {
                "1234": Item(Status.TODO, "Barry"),
            },
            id="Gets name from JSON and looks up list",
        ),
        pytest.param(
            [
                {"id": "1234", "idList": "111", "name": "Barry"},
                {"id": "1235", "idList": "112", "name": "Jerry"},
            ],
            {
                "1234": Item(Status.TODO, "Barry"),
                "1235": Item(Status.DONE, "Jerry"),
            },
            id="Correctly decodes multiple items with different lists",
        ),
    ],
)
def test_items_from_json(lists, as_json, expected: Dict):
    assert items_from_json(lists, as_json) == expected


@pytest.mark.parametrize(
    "as_json,expected",
    [
        pytest.param(
            [{"id": "1234", "name": "TO DO"}],
            {
                "1234": TrelloList("TO DO"),
            },
            id="Gets name and id from JSON",
        ),
        pytest.param(
            [{"id": "1234", "name": "TO DO"}, {"id": "1235", "name": "DONE"}],
            {
                "1234": TrelloList("TO DO"),
                "1235": TrelloList("DONE"),
            },
            id="Correctly decodes multiple items with different lists",
        ),
    ],
)
def test_trello_lists_from_json(as_json, expected: Dict):
    assert trello_lists_from_json(as_json) == expected
