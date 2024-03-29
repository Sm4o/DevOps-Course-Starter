from datetime import datetime

from flask_login import current_user

from todo_app.views.views import ViewModel
from todo_app.data.mongodb import CardStatus
from todo_app.data.item import Item
from todo_app.app import WRITER_LIST


def test_filter_items():
    items = [
        Item('1', 'item1', 'description1', CardStatus.TODO, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('2', 'item2', 'description2', CardStatus.TODO, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('3', 'item3', 'description3', CardStatus.DOING, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('4', 'item4', 'description4', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
    ]
    item_view_model = ViewModel(items, current_user, WRITER_LIST)
    assert item_view_model.items_todo == items[:2] 
    assert item_view_model.items_doing == [items[2]]
    assert item_view_model.items_done == items[-1:]


def test_show_all_done_items_is_true_for_fewer_than_five_cards():
    """ Only show all done items if less than 5 done items """
    items = [
        Item('1', 'item', 'description', CardStatus.DOING, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('2', 'item', 'description', CardStatus.TODO, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('3', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
    ]
    item_view_model = ViewModel(items, current_user, WRITER_LIST)
    assert item_view_model.show_all_done_items == True


def test_show_all_done_items_is_false_for_five_or_more_cards():
    items = [
        Item('1', 'item', 'description', CardStatus.DOING, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('2', 'item', 'description', CardStatus.TODO, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('3', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('4', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('5', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('6', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('7', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
    ]
    item_view_model = ViewModel(items, current_user, WRITER_LIST)
    assert item_view_model.show_all_done_items == False 


def test_recent_done_items():
    """ Only show tasks done today """
    items = [
        Item('1', 'item', 'description', CardStatus.DOING, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('2', 'item', 'description', CardStatus.TODO, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('3', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('4', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('5', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('6', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('7', 'item', 'description', CardStatus.DONE, datetime.utcnow()),
    ]
    item_view_model = ViewModel(items, current_user, WRITER_LIST)
    assert item_view_model.recent_done_items == [items[-1]] 


def test_older_done_items():
    items = [
        Item('1', 'item', 'description', CardStatus.DOING, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('2', 'item', 'description', CardStatus.TODO, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('3', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('4', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('5', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('6', 'item', 'description', CardStatus.DONE, datetime.strptime('2021-03-31T16:47:17.915Z', '%Y-%m-%dT%H:%M:%S.%fZ')),
        Item('7', 'item', 'description', CardStatus.DONE, datetime.utcnow()),
    ]
    item_view_model = ViewModel(items, current_user, WRITER_LIST)
    assert item_view_model.older_done_items == items[2:6] 
