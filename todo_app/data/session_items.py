from __future__ import annotations
from typing import Callable, Dict, Optional
from flask import session
from dataclasses import dataclass


@dataclass
class Item:
    status: str
    title: str


class Items:
    _items_by_id: Dict[int, Item]
    _next_item_id: int

    def __init__(self, items_by_id: Dict[int, Item], next_item_id: int) -> None:
        self._items_by_id = items_by_id
        self._next_item_id = next_item_id

    def items(self):
        return self._items_by_id.items()

    def default() -> Items:
        ret = Items(items_by_id={}, next_item_id=0)
        for item in _DEFAULT_ITEMS:
            ret.add(item)
        return ret

    def add(self, item: Item):
        next_id = self._next_item_id
        self._next_item_id += 1
        self._items_by_id[next_id] = item

    def update(self, id: int, item: Item):
        old_item = self.remove(id)
        if old_item is None:
            raise ValueError("Cannot update an item that does not exist!")
        self._items_by_id[id] = item

    def get(self, id: int) -> Optional[Item]:
        return self._items_by_id.get(id)

    def get_or_throw(self, id: int) -> Item:
        item = self.get(id)
        if item is None:
            raise ValueError(
                f"Could not find an item with id {id} - acceptable {self._items_by_id.keys()}"
            )
        return item

    def remove(self, id: int) -> Optional[Item]:
        return self._items_by_id.pop(id)

    def save(self):
        session["_items_by_id"] = self._items_by_id
        session["_next_item_id"] = self._next_item_id

    def load() -> Optional[Items]:
        next_item_id_as_string = session.get("_next_item_id")
        if next_item_id_as_string is None:
            return None
        next_item_id = int(next_item_id_as_string)
        items_by_id_as_strings: Dict[str, Dict[str, str]] = session.get("_items_by_id")
        items_by_id = {}
        for key, value in items_by_id_as_strings.items():
            items_by_id[int(key)] = Item(value["status"], value["title"])
        return Items(items_by_id=items_by_id, next_item_id=next_item_id)


_DEFAULT_ITEMS = [
    Item(status="Not Started", title="List saved todo items"),
    Item(status="Not Started", title="Allow new items to be added"),
]


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        Items: The saved items, or a default if none present.
    """
    return Items.load() or Items.default()


def get_item(id: int):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return items.get(id)


def get_item_or_throw(id: int):
    """
        Fetch saved item with given id, throwing an error if no such item exists
    """
    items = get_items()
    return items.get_or_throw(id)


def add_item(title: str):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    item = {"title": title, "status": "Not Started"}

    items.add(item)

    items.save()

    return item


def delete_item(id: int):
    """
    Delete a saved item by id
    """
    items = get_items()
    items.remove(id)
    items.save()


def update_item(id: int, update_func: Callable[[Item], Item]):
    items = get_items()

    item = items.get_or_throw(id)

    updated = update_func(item)

    items.update(id, updated)

    items.save()


def complete_item(id: int):
    def update(item):
        item.status = "Completed"
        return item

    update_item(id, update)


def uncomplete_item(id: int):
    def update(item):
        item.status = "Not started"
        return item

    update_item(id, update)
