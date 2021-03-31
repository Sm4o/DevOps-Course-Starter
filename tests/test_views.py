from todo_app.views.views import ViewModel
from todo_app.data.trello import CardStatus
from todo_app.data.item import Item


def test_filter_items():
    items = [
        Item('1', 'item1', 'description1', CardStatus.TODO),
        Item('2', 'item2', 'description2', CardStatus.TODO),
        Item('3', 'item3', 'description3', CardStatus.DOING),
        Item('4', 'item4', 'description4', CardStatus.DONE),
    ]
    item_view_model = ViewModel(items)
    assert item_view_model.items_todo == items[:2] 
    assert item_view_model.items_doing == [items[2]]
    assert item_view_model.items_done == items[-1:]