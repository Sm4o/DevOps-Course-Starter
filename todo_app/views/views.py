from typing import List
from datetime import datetime

from todo_app.data.trello import CardStatus
from todo_app.data.item import Item

# Annotations only
from enum import Enum


class ViewModel:
    def __init__(self, items: List[Item]):
        self._items = items
        self._items_todo = None 
        self._items_done = None
        self._items_doing = None
        self._show_all_done_items = None 
        self._recent_done_items = None
        self._older_done_itmes = None

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

    @property
    def show_all_done_items(self):
        return True if len(self.items_done) < 5 else False

    @property
    def recent_done_items(self):
        recent_items = []
        for item in self.items_done:
            item_date = datetime.strptime(item.last_modified_date, '%Y-%m-%dT%H:%M:%S.%fZ').date()
            if item_date == datetime.today().date() or self.show_all_done_items:
                recent_items.append(item)
        return recent_items

    @property
    def older_done_items(self):
        older_items = []
        for item in self.items_done:
            item_date = datetime.strptime(item.last_modified_date, '%Y-%m-%dT%H:%M:%S.%fZ').date() 
            if item_date != datetime.today().date() and not self.show_all_done_items:
                older_items.append(item)
        return older_items

    def _filter_items(self, status: Enum) -> List[Item]:
        return [item for item in self.items if item.status.value == status.value]
