from typing import List, Any
from datetime import datetime

from todo_app.data.mongodb import CardStatus
from todo_app.data.item import Item

# Annotations only
from enum import Enum


class ViewModel:
    def __init__(
        self, 
        items: List[Item], 
        current_user: Any, 
        writer_list: List[str],
        login_disabled: bool=False,
    ):
        self._items = items
        self._current_user = current_user
        self._writer_list= writer_list
        self.login_disabled = login_disabled

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
            if item.last_modified_date.date() == datetime.today().date() or self.show_all_done_items:
                recent_items.append(item)
        return recent_items

    @property
    def older_done_items(self):
        older_items = []
        for item in self.items_done:
            if item.last_modified_date.date() != datetime.today().date() and not self.show_all_done_items:
                older_items.append(item)
        return older_items
    
    @property
    def can_see_write_controls(self):
        if self.login_disabled:
            return True
        elif self._current_user.id in self._writer_list:
            return True
        else:
            return False

    def _filter_items(self, status: Enum) -> List[Item]:
        return [item for item in self.items if item.status.value == status.value]
