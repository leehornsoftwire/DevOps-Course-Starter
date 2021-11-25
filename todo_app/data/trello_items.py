from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Optional


import requests

from todo_app.data.items_backend import Item, ItemsBackend

APP_TOKEN = "e7484da444a424b051ef7b0e0803de690b3242cdfd55137f9269894a8095adbd"
KEY = os.environ["TRELLO_KEY"]
BOARD_ID = "iFh8nAOF"
BASE_URL = "https://api.trello.com/1"

COMMON_PARAMS = {"token": APP_TOKEN, "key": KEY}



class TrelloItems(ItemsBackend):
    def load() -> ItemsBackend:
        return TrelloItems()
    def get_items(self) -> Dict[str, Item]:
        params = COMMON_PARAMS
        url = f"{BASE_URL}/boards/{BOARD_ID}/cards"
        lists = get_lists()
        cards_as_json = requests.get(url, params).json()
        return {as_json["id"]: item_from_json(lists, as_json) for as_json in cards_as_json}

    def add_item(self, item: Item):
        params = {**COMMON_PARAMS, "name": item.title, "idList": get_list_id_by_name(item.status)}
        url = f"{BASE_URL}/cards"
        requests.post(url, params=params)
        
    def delete_item(self, id: str):
        params = COMMON_PARAMS
        url = f"{BASE_URL}/cards/{id}"
        requests.delete(url, params=params)

    def complete_item(self, id: str):
        send_item_to_list(id, "DONE")

    def uncomplete_item(self, id: str):
        send_item_to_list(id, "TO DO")

def item_from_json(lists: Dict[str, str], as_json: Dict) -> Item:
    in_list = lists[as_json["idList"]]
    return Item(in_list, as_json["name"])
def get_lists() -> Dict[str, str]:
        url = f"{BASE_URL}/boards/{BOARD_ID}/lists"
        params = COMMON_PARAMS
        lists_as_json = requests.get(url, params).json()
        return {list_["id"]: list_["name"] for list_ in lists_as_json}
def get_list_id_by_name(name: str):
    params = COMMON_PARAMS
    url = f"{BASE_URL}/boards/{BOARD_ID}/lists"
    lists_as_json: List[Dict] = requests.get(url, params).json()
    for list in lists_as_json:
        if list["name"] == name:
            return list["id"]
    raise ValueError(f"No board with name {name} found!")

def send_item_to_list(id: str, list_name: str):
    url = f"{BASE_URL}/cards/{id}"
    completed_list_id = get_list_id_by_name(list_name)
    params = {**COMMON_PARAMS, "idList": completed_list_id}
    requests.put(url, params=params)