from typing import List

from flask import session

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]


def get_items() -> List[dict]:
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    items = session.get('items', _DEFAULT_ITEMS)
    sorted_items = sorted(items, key=lambda item: item['status'], reverse=True) 
    return sorted_items


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
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    try:
        id = max([item['id'] for item in items]) + 1
    except ValueError:
        # No items hence start from ID 1
        id = 1

    item = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    items.insert(0, item)
    session['items'] = items


def save_item(item: dict) -> None:
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items


def delete_item(item_id: int) -> None:
    """
    Deletes an item from the session. 
    If the item doesn't exist it will skip.

    Args:
        item_id: The ID of the item to delete. 

    Returns:
        item_id: The ID of the item deleted.
    """
    existing_items = get_items()

    updated_items = list(filter(None, [existing_items if existing_items['id'] != item_id else None for existing_items in existing_items]))

    session['items'] = updated_items
