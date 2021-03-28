from enum import Enum
from typing import List

import requests

from todo_app.data.item import Item


class CardStatus(Enum):
    # TODO: What if we rename on Trello the board? hmm. Use auto()?
    DONE = 'Done'
    TODO = 'To Do'


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
        cards = self.get_board_cards()
        for card in cards:
            for todo_list in self.board_lists:
                if card['idList'] == todo_list['id']:
                    card['status'] = todo_list['name']

        cards = [card for card in cards if card['idList']]
        sorted_cards = sorted(cards, key=lambda card: card['status'], reverse=True) 
        return sorted_cards

    def get_board_cards(self) -> List[dict]:
        endpoint = f"boards/{self.board_id}/cards"
        params = {
            'key': self.app_key,
            'token': self.token,
        }
        resp = requests.get(self.BASE_URL + endpoint, params=params)
        return resp.json()

    def get_board_lists(self) -> List[dict]:
        endpoint = f"boards/{self.board_id}/lists"
        params = {
            'key': self.app_key,
            'token': self.token,
        }
        resp = requests.get(self.BASE_URL + endpoint, params=params)
        return resp.json()

    def add_item(self, name: str) -> None:
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
