import os
from enum import Enum
from datetime import datetime
from typing import List

import pymongo
from bson.objectid import ObjectId

from todo_app.data.item import Item


class CardStatus(Enum):
    DONE = 'Done'
    TODO = 'To Do'
    DOING = 'Doing'

    @classmethod
    def get_status(cls, status: str) -> Enum:
        if status == cls.DONE.value:
            return cls.DONE
        elif status == cls.TODO.value:
            return cls.TODO
        elif status == cls.DOING.value:
            return cls.DOING
        else:
            raise ValueError('Unknown status')


class MongoDB:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.environ.get('DB_CONNECTION'))
        self.items = self.client[os.environ.get("DATABASE_NAME")].items

    def get_items(self) -> List[dict]:
        """
        Fetches all saved items. 

        Returns:
            list: The list of saved items.
        """
        item_list = []
        for item in self.items.find():
            id = item['_id']
            title = item['name']
            description = item['desc']
            status = CardStatus.get_status(item['status'])
            last_modified_date = item['dateLastActivity']
            item_list.append(Item(id, title, description, status, last_modified_date))

        sorted_cards = sorted(item_list, key=lambda card: card.status.value, reverse=True) 
        return sorted_cards

    def add_item(self, name: str, description: str) -> None:
        """
        Add a new item with the specified title

        Args:
            name: The name of the item.
        """
        item = {
            'status': 'To Do',
            'name': name,
            'desc': description,
            'dateLastActivity': datetime.utcnow()
        }
        self.items.insert_one(item)

    def delete_item(self, item_id: str) -> None:
        """
        Delete an item 
        If the item doesn't exist it will skip.

        Args:
            item_id: The ID of the item to delete. 
        """
        self.items.delete_one({"_id": ObjectId(item_id)})

    def update_item(self, item_id: str, status: Enum) -> None:
        """
        Update card status

        Args:
            item_id: The ID of the item to update.
            status: Instance of CardStatus Enum class.
        """
        item = {
            "$set": {
                'status': status.value,
                'dateLastActivity': datetime.utcnow()
            }
        }
        self.items.update_one({'_id': ObjectId(item_id)}, item)
