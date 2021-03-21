from typing import List

from flask import session

from todo_app.trello import (
    get_board_lists, 
    get_board_cards,
    create_card,
    delete_card,
    mark_card_as_done,
    mark_card_as_todo,
)


def get_items() -> List[dict]:
    """
    Fetches all saved items from the Trello. 

    Returns:
        list: The list of saved items.
    """
    todo_lists = get_board_lists()
    cards = get_board_cards()
    for card in cards:
        for todo_list in todo_lists:
            if card['idList'] == todo_list['id']:
                card['status'] = todo_list['name']

    cards = [card for card in cards if card['idList']]
    sorted_cards = sorted(cards, key=lambda card: card['status'], reverse=True) 
    return sorted_cards


def get_item(id: int) -> dict:
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title: str) -> None:
    """
    Adds a new item with the specified title to the Trello.

    Args:
        title: The title of the item.
    """
    create_card(title)


def delete_item(item_id: str) -> None:
    """
    Deletes an item from Trello. 
    If the item doesn't exist it will skip.

    Args:
        item_id: The ID of the item to delete. 

    Returns:
        item_id: The ID of the item deleted.
    """
    delete_card(item_id)


def update_item_complete(item_id: str) -> None:
    mark_card_as_done(item_id)


def update_item_uncomplete(item_id: str) -> None:
    mark_card_as_todo(item_id)