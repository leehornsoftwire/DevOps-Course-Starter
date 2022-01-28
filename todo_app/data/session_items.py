from __future__ import annotations

from functools import wraps
from typing import Dict, Optional

from flask import session

from todo_app.data.items_backend import Item, ItemsBackend, Status


def save_after(func):
    @wraps(func)
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
    def set_status(self, id: str, status: Status):
        self._items_by_id[id].status = status

    def serialisable_items(self) -> Dict:
        return {id: serialisable_item(item) for id, item in self._items_by_id.items()}

    def save(self):
        session["_items_by_id"] = self.serialisable_items()
        session["_next_item_id"] = self._next_item_id

    @classmethod
    def load(cls) -> ItemsBackend:
        next_item_id_as_string = session.get("_next_item_id")
        if next_item_id_as_string is None:
            return cls({}, 0)
        next_item_id = int(next_item_id_as_string)
        items_by_id_as_strings: Dict[str, Dict[str, str]] = session.get("_items_by_id")
        items_by_id = {}
        for key, value in items_by_id_as_strings.items():
            items_by_id[key] = Item(Status(value["status"]), value["title"])
        return cls(items_by_id=items_by_id, next_item_id=next_item_id)


def serialisable_item(item: Item) -> Dict:
    return {"title": item.title, "status": item.status.value}
