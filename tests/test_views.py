from datetime import datetime

from todo_app.views.views import ViewModel
from todo_app.data.trello import CardStatus
from todo_app.data.item import Item


def test_filter_items():
    items = [
        Item('1', 'item1', 'description1', CardStatus.TODO, '2021-03-31T16:47:17.915Z'),
        Item('2', 'item2', 'description2', CardStatus.TODO, '2021-03-31T16:47:17.915Z'),
        Item('3', 'item3', 'description3', CardStatus.DOING, '2021-03-31T16:47:17.915Z'),
        Item('4', 'item4', 'description4', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
    ]
    item_view_model = ViewModel(items)
    assert item_view_model.items_todo == items[:2] 
    assert item_view_model.items_doing == [items[2]]
    assert item_view_model.items_done == items[-1:]


def test_show_all_done_items():
    """ Only show all done items if less than 5 done items """
    items = [
        Item('1', 'item', 'description', CardStatus.DOING, '2021-03-31T16:47:17.915Z'),
        Item('2', 'item', 'description', CardStatus.TODO, '2021-03-31T16:47:17.915Z'),
        Item('3', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
    ]
    item_view_model = ViewModel(items)
    assert item_view_model.show_all_done_items == True

    items = [
        Item('1', 'item', 'description', CardStatus.DOING, '2021-03-31T16:47:17.915Z'),
        Item('2', 'item', 'description', CardStatus.TODO, '2021-03-31T16:47:17.915Z'),
        Item('3', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('4', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('5', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('6', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('7', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
    ]
    item_view_model = ViewModel(items)
    assert item_view_model.show_all_done_items == False 


def test_recent_done_items():
    """ Only show tasks done today """
    items = [
        Item('1', 'item', 'description', CardStatus.DOING, '2021-03-31T16:47:17.915Z'),
        Item('2', 'item', 'description', CardStatus.TODO, '2021-03-31T16:47:17.915Z'),
        Item('3', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('4', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('5', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('6', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('7', 'item', 'description', CardStatus.DONE, datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
    ]
    item_view_model = ViewModel(items)
    assert item_view_model.recent_done_items == [items[-1]] 


def test_older_done_items():
    items = [
        Item('1', 'item', 'description', CardStatus.DOING, '2021-03-31T16:47:17.915Z'),
        Item('2', 'item', 'description', CardStatus.TODO, '2021-03-31T16:47:17.915Z'),
        Item('3', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('4', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('5', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('6', 'item', 'description', CardStatus.DONE, '2021-03-31T16:47:17.915Z'),
        Item('7', 'item', 'description', CardStatus.DONE, datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
    ]
    item_view_model = ViewModel(items)
    assert item_view_model.older_done_items == items[2:6] 
