from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Item:
    status: str
    title: str


class ItemsBackend:
    def load() -> ItemsBackend:
        pass

    def get_items() -> Dict[str, Item]:
        pass

    def add_item(item: Item):
        pass

    def delete_item(id: str):
        pass

    def complete_item(id: str):
        pass

    def uncomplete_item(id: str):
        pass
