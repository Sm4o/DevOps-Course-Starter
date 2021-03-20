from typing import List

from flask import session

from todo_app.trello import (
    get_board_lists, 
    get_board_cards,
    create_card,
    delete_card,
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


def save_item(item: dict) -> None:
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items


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
