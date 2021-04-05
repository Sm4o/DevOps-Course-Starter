import os
from unittest.mock import Mock, patch 

import pytest
from dotenv import find_dotenv, load_dotenv

from todo_app import app

TEST_BOARD_ID = os.environ.get('BOARD_ID')


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests
    with test_app.test_client() as client:
        yield client


def mock_get_lists():
    response = Mock()
    response.json.return_value = [
        {
            "id": "12345678",
            "name": "To Do",
            "idBoard": "0123456789",
            "subscribed": False
        },
    ]
    return response


def mock_get_cards(url, params):
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/cards':
        response = Mock()
        response.json.return_value = [
            {
                "id": "6066013f36c018688008c0f3",
                "name": "name",
                "desc": "description",
                "dateLastActivity": "2021-04-01T17:36:01.339Z",
                "idBoard": "604e8d8f40bbb0669d50314b",
                "idList": "604e8d8f40bbb0669d50314e",
                "dueComplete": False,
                "due": None,
            },
        ]
        return response

    return None

@patch('todo_app.app.Trello')
@patch('requests.get')  
def test_index_page(mock_get_requests, mock_trello, client):
    mock_trello.get_board_lists.side_effect = mock_get_lists 
    mock_get_requests.side_effect = mock_get_cards
    response = client.get('/')
    assert 'name - description' in response.get_data(as_text=True)


@patch('todo_app.app.Trello')
@patch('requests.post')  
@patch('requests.get')  
def test_add_todo_item(mock_get_requests, mock_post_requests, mock_trello, client):
    mock_trello.get_board_lists.side_effect = mock_get_lists 
    mock_post_requests.side_effect = None 
    mock_get_requests.side_effect = mock_get_cards

    response = client.post('/add_item', data=dict(
        title='name',
        description='description',
    ), follow_redirects=True)
    assert 'name - description' in response.get_data(as_text=True)


@patch('todo_app.app.Trello')
@patch('requests.get')  
def test_complete_item(mock_get_requests, mock_trello, client):
    mock_trello.get_board_lists.side_effect = mock_get_lists 
    mock_get_requests.side_effect = mock_get_cards

    response = client.get('/complete/1', follow_redirects=True)
    assert 'name - description' in response.get_data(as_text=True)

@patch('todo_app.app.Trello')
@patch('requests.get')  
def test_do_item(mock_get_requests, mock_trello, client):
    mock_trello.get_board_lists.side_effect = mock_get_lists 
    mock_get_requests.side_effect = mock_get_cards

    response = client.get('/do/1', follow_redirects=True)
    assert 'name - description' in response.get_data(as_text=True)


@patch('todo_app.app.Trello')
@patch('requests.get')  
def test_uncomplete_item(mock_get_requests, mock_trello, client):
    mock_trello.get_board_lists.side_effect = mock_get_lists 
    mock_get_requests.side_effect = mock_get_cards

    response = client.get('/uncomplete/1', follow_redirects=True)
    assert 'name - description' in response.get_data(as_text=True)


@patch('todo_app.app.Trello')
@patch('requests.get')  
def test_remove_item(mock_get_requests, mock_trello, client):
    mock_trello.get_board_lists.side_effect = mock_get_lists 
    mock_get_requests.side_effect = mock_get_cards

    response = client.get('/delete/1', follow_redirects=True)
    assert 'name - description' in response.get_data(as_text=True)
