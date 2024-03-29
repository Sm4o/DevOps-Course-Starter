import os
import pytest
from dotenv import find_dotenv, load_dotenv
import mongomock
import pymongo
from bson.objectid import ObjectId

from todo_app import app


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        prepare_test_data()
        test_app = app.create_app()
        test_app.config['LOGIN_DISABLED'] = True
        with test_app.test_client() as client:
            yield client


def test_index_page(client):
    response = client.get('/')
    response_text = response.get_data(as_text=True)
    assert 'Do Corndel project exercises!' in response_text
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 


def test_add_todo_item(client):
    response = client.post('/add_item', data=dict(
        title='Do laundry',
        description='description',
    ), follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 
    assert 'Do laundry' in response_text 


def test_complete_item(client):
    response = client.get(f'/complete/61a7fab58503e36eb7595414', follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No items to do yet' in response_text
    assert 'No items in progress' in response_text 
    assert 'No recent items completed yet' not in response_text 


def test_do_item(client):
    response = client.get('/do/61a7fab58503e36eb7595414', follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No items to do yet' in response_text
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' not in response_text 


def test_uncomplete_item(client):
    response = client.get('/uncomplete/61a7fab58503e36eb7595414', follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No items to do yet' not in response_text 
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 



def test_remove_item(client):
    response = client.get('/delete/61a7fab58503e36eb7595414', follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No items to do yet' in response_text 
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 


def prepare_test_data():
    item = {
        "_id": ObjectId("61a7fab58503e36eb7595414"),
        "name": "Do Corndel project exercises!", 
        "desc": "description",
        "status": "To Do", 
        "dateLastActivity": "2022-01-01T22:22:22.1111Z"
    }
    mongo_client = pymongo.MongoClient(os.environ.get('DB_CONNECTION'))
    items = mongo_client[os.environ.get('DATABASE_NAME')].items
    items.insert_one(item)
