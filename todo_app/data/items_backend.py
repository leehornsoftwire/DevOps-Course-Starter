from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class Status(Enum):
    TODO = "To do"
    DOING = "Doing"
    DONE = "Done"


@dataclass
class Item:
    status: Status
    title: str


class ItemsBackend:
    def load() -> ItemsBackend:
        pass

    def get_items(self) -> Dict[str, Item]:
        pass

    def get_items_by_status(self, status: Status) -> Dict[str, Item]:
        return {k: v for k, v in self.get_items().items() if v.status == status}

    def add_item(self, item: Item):
        pass

    def delete_item(self, id: str):
        pass

    def set_status(self, id: str, status: Status):
        pass
