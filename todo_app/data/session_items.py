from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional

from flask import session

from todo_app.data.items_backend import Item, ItemsBackend


def save_after(func):
    def func_and_save(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.save()
        return result

    return func_and_save


class SessionItems(ItemsBackend):
    _items_by_id: Dict[str, Item]
    _next_item_id: int

    def __init__(self, items_by_id: Dict[str, Item], next_item_id: int) -> None:
        self._items_by_id = items_by_id
        self._next_item_id = next_item_id

    def get_items(self) -> Dict[str, Item]:
        return self._items_by_id

    @save_after
    def add_item(self, item: Item):
        next_id = str(self._next_item_id)
        self._next_item_id += 1
        self._items_by_id[next_id] = item

    @save_after
    def delete_item(self, id: str) -> Optional[Item]:
        return self._items_by_id.pop(id)

    @save_after
    def complete_item(self, id: str):
        self._items_by_id[id].status = "DONE"

    @save_after
    def uncomplete_item(self, id: str):
        self._items_by_id[id].status = "TO DO"

    def save(self):
        session["_items_by_id"] = self._items_by_id
        session["_next_item_id"] = self._next_item_id

    def load() -> ItemsBackend:
        next_item_id_as_string = session.get("_next_item_id")
        if next_item_id_as_string is None:
            return SessionItems({}, 0)
        next_item_id = int(next_item_id_as_string)
        items_by_id_as_strings: Dict[str, Dict[str, str]] = session.get("_items_by_id")
        items_by_id = {}
        for key, value in items_by_id_as_strings.items():
            items_by_id[key] = Item(value["status"], value["title"])
        return SessionItems(items_by_id=items_by_id, next_item_id=next_item_id)
