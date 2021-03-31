from enum import Enum
from typing import List

import requests

from todo_app.data.item import Item


class CardStatus(Enum):
    DONE = 'Done'
    TODO = 'To Do'
    DOING = 'Doing'

    @classmethod
    def get_status(cls, list_id: str, board_lists: List[dict]) -> Enum:
        status = next((list['name'] for list in board_lists if list['id'] == list_id), None)
        if status == cls.DONE.value:
            return cls.DONE
        elif status == cls.TODO.value:
            return cls.TODO
        elif status == cls.DOING.value:
            return cls.DOING
        else:
            raise ValueError('Unknown status')


class Trello:
    BASE_URL = "https://api.trello.com/1/"

    def __init__(self, app_key: str, token: str, board_id: str) -> None:
        self.app_key = app_key
        self.token = token
        self.board_id = board_id
        self.board_lists = self.get_board_lists()

    def get_items(self) -> List[dict]:
        """
        Fetches all saved items from Trello. 

        Returns:
            list: The list of saved items.
        """
        endpoint = f"boards/{self.board_id}/cards"
        params = {
            'key': self.app_key,
            'token': self.token,
        }

        cards = []
        json_response = requests.get(self.BASE_URL + endpoint, params=params).json()
        for card in json_response:
            id = card['id']
            title = card['name']
            description = card['desc']
            list_id = card['idList'] 
            status = CardStatus.get_status(list_id, self.board_lists)
            cards.append(Item(id, title, description, status))

        sorted_cards = sorted(cards, key=lambda card: card.status.value, reverse=True) 
        return sorted_cards

    def get_board_lists(self) -> List[dict]:
        endpoint = f"boards/{self.board_id}/lists"
        params = {
            'key': self.app_key,
            'token': self.token,
        }
        resp = requests.get(self.BASE_URL + endpoint, params=params)
        return resp.json()

    def add_item(self, name: str, description: str) -> None:
        """
        Add a new item with the specified title to the Trello.

        Args:
            name: The name of the item.
        """
        endpoint = "cards"
        todo_list = next((list for list in self.board_lists if list['name'] == CardStatus.TODO.value), None)
        params = {
            'key': self.app_key,
            'token': self.token,
            'name': name,
            'desc': description,
            'idList': todo_list['id'],
        }
        resp = requests.post(self.BASE_URL + endpoint, params=params)
        return resp.json()    

    def delete_item(self, card_id: str) -> None:
        """
        Delete a card from Trello. 
        If the card doesn't exist it will skip.

        Args:
            card_id: The ID of the card to delete. 
        """
        endpoint = f"cards/{card_id}"
        params = {
            'key': self.app_key,
            'token': self.token,
        }
        requests.delete(self.BASE_URL + endpoint, params=params)

    def update_item(self, card_id: str, status: Enum) -> None:
        """
        Update card status

        Args:
            card_id: The ID of the card to update.
            status: Instance of CardStatus Enum class.
        """
        endpoint = f"cards/{card_id}"
        done_list = next((list for list in self.board_lists if list['name'] == status.value), None)
        params = {
            'key': self.app_key,
            'token': self.token,
            'id': card_id,
            'idList': done_list['id'],
        }
        requests.put(self.BASE_URL + endpoint, params=params)
