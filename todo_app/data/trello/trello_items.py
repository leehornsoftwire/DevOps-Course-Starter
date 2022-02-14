import os
from dataclasses import dataclass
from typing import Dict

import more_itertools

from todo_app.data.items_backend import Item, ItemsBackend, Status
from todo_app.data.trello.trello_request import TrelloRequest


@dataclass
class TrelloItem(Item):
    list_id: str


@dataclass(frozen=True)
class TrelloList:
    name: str


@dataclass
class TrelloItems(ItemsBackend):
    app_token: str
    key: str
    board_id: str

    def get_name(self) -> str:
        return "Trello"

    @classmethod
    def load_environment(cls) -> ItemsBackend:
        app_token = os.environ["TRELLO_TOKEN"]
        key = os.environ["TRELLO_KEY"]
        board_id = os.environ["TRELLO_BOARD"]
        return cls(app_token, key, board_id)

    @classmethod
    def load(cls) -> ItemsBackend:
        ret = cls.load_environment()
        ret.create_missing_lists()
        return ret

    def create_missing_lists(self):
        existing_lists = {list.name for list in self.get_lists().values()}
        required_lists = set(LIST_NAME_TO_STATUS.keys())
        to_add = required_lists.difference(existing_lists)
        for required_name in to_add:
            self.get_trello_request("lists").with_params(
                {"name": required_name, "idBoard": self.board_id}
            ).post()

    def get_trello_request(self, relative_url: str) -> TrelloRequest:
        return TrelloRequest.new(self.app_token, self.key).with_url(relative_url)

    def get_trello_request_for_board(self, relative_url: str) -> TrelloRequest:
        return self.get_trello_request(f"boards/{self.board_id}").with_url(relative_url)

    def get_items(self) -> Dict[str, Item]:
        cards_as_json = self.get_trello_request_for_board("cards").get().json()
        lists = self.get_lists()
        return items_from_json(lists, cards_as_json)

    def get_items_by_status(self, status: Status):
        lists = self.get_lists()
        list_name = status_to_list_name(status)
        try:
            list_id = get_list_id_from_lists_and_name(lists, list_name)
        except ValueError:
            raise ValueError(f"No list with name {list_name} in {lists}")
        cards_as_json = self.get_trello_request(f"lists/{list_id}/cards").get().json()
        return items_from_json(lists, cards_as_json)

    def add_item(self, item: Item):
        lists = self.get_lists()
        list_id = get_list_id_from_lists_and_name(
            lists, status_to_list_name(item.status)
        )
        self.get_trello_request("cards").with_params(
            {
                "name": item.title,
                "idList": list_id,
            }
        ).post()

    def delete_item(self, id: str):
        self.get_trello_request(f"cards/{id}").delete()

    def set_status(self, id: str, status: Status):
        self.send_item_to_list(id, status_to_list_name(status))

    def get_lists(self) -> Dict[str, TrelloList]:
        lists_as_json = self.get_trello_request_for_board("lists").get().json()
        return trello_lists_from_json(lists_as_json)

    def send_item_to_list(self, card_id: str, list_name: str):
        lists = self.get_lists()
        completed_list_id = get_list_id_from_lists_and_name(lists, list_name)
        self.get_trello_request(f"cards/{card_id}").with_params(
            {"idList": completed_list_id}
        ).put()

    def delete_board(self):
        self.get_trello_request(f"boards/{self.board_id}").delete()


def trello_lists_from_json(lists_as_json: Dict) -> Dict[str, TrelloList]:
    return {list_["id"]: TrelloList(list_["name"]) for list_ in lists_as_json}


def items_from_json(lists: Dict[str, str], cards_as_json: Dict) -> Dict[str, Item]:
    return {as_json["id"]: item_from_json(lists, as_json) for as_json in cards_as_json}


LIST_NAME_TO_STATUS = {"TO DO": Status.TODO, "DONE": Status.DONE, "DOING": Status.DOING}
STATUS_TO_LIST_NAME = {v: k for k, v in LIST_NAME_TO_STATUS.items()}


def list_name_to_status(list_name: str) -> Status:
    return LIST_NAME_TO_STATUS[list_name]


def status_to_list_name(status: Status) -> str:
    return STATUS_TO_LIST_NAME[status]


def get_list_id_from_lists_and_name(lists: Dict[str, TrelloList], list_name: str):
    return more_itertools.one(
        (id for id, list in lists.items() if list.name == list_name)
    )


def item_from_json(lists: Dict[str, TrelloList], as_json: Dict) -> Item:
    in_list = lists[as_json["idList"]]
    return Item(list_name_to_status(in_list.name), as_json["name"])
