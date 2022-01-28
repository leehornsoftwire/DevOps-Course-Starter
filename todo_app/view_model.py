from typing import Dict
from todo_app.data.items_backend import Item, ItemsBackend, Status


class ViewModel:
    def __init__(self, items_backend: ItemsBackend) -> None:
        self.items_backend = items_backend
        self.Status = Status  # so the enum can be accessed from the template - imports cannot be used

    def get_item_backend_name(self) -> str:
        return type(self.items_backend).__name__

    def todo_items(self) -> Dict[str, Item]:
        return self.items_backend.get_items_by_status(Status.TODO)

    def doing_items(self) -> Dict[str, Item]:
        return self.items_backend.get_items_by_status(Status.DOING)

    def done_items(self) -> Dict[str, Item]:
        return self.items_backend.get_items_by_status(Status.DONE)
