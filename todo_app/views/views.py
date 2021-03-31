from todo_app.data.trello import CardStatus
from typing import List
from todo_app.data.item import Item

# Annotations only
from enum import Enum


class ViewModel:
    def __init__(self, items: List[Item]):
        self._items = items
        self._items_todo = None 
        self._items_done = None
        self._items_doing = None

    @property
    def items(self):
        return self._items

    @property
    def items_todo(self):
        return self._filter_items(CardStatus.TODO)

    @property
    def items_done(self):
        return self._filter_items(CardStatus.DONE)

    @property
    def items_doing(self):
        return self._filter_items(CardStatus.DOING)

    def _filter_items(self, status: Enum) -> List[Item]:
        return [item for item in self.items if item.status.value == status.value]
