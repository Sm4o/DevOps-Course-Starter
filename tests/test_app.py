import os
from unittest.mock import Mock, patch 

import pytest
from dotenv import find_dotenv, load_dotenv

from todo_app import app


def mock_get_response(url, params):
    TEST_BOARD_ID = os.environ.get('BOARD_ID')

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
    elif url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()
        response.json.return_value = [
            {
                "id": "604e8d8f40bbb0669d50314e",
                "name": "To Do",
                "idBoard": "0123456789",
                "subscribed": False
            },
            {
                "id": "DoneID",
                "name": "Done",
                "idBoard": "0123456789",
                "subscribed": False
            },
            {
                "id": "DoingID",
                "name": "Doing",
                "idBoard": "0123456789",
                "subscribed": False
            },
        ]
        return response
    return None


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app
    with patch('requests.get') as mock_get_requests:
        mock_get_requests.side_effect = mock_get_response
        test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests
    with test_app.test_client() as client:
        yield client


@patch('requests.get')  
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_response
    response = client.get('/')
    response_text = response.get_data(as_text=True)
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 


@patch('requests.post')  
@patch('requests.get')  
def test_add_todo_item(mock_get_requests, mock_post_requests, client):
    mock_post_requests.side_effect = None 
    mock_get_requests.side_effect = mock_get_response

    response = client.post('/add_item', data=dict(
        title='name',
        description='description',
    ), follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 


@patch('requests.get')  
def test_complete_item(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_response

    response = client.get('/complete/1', follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 


@patch('requests.get')  
def test_do_item(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_response

    response = client.get('/do/1', follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 


@patch('requests.get')  
def test_uncomplete_item(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_response

    response = client.get('/uncomplete/1', follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 


@patch('requests.get')  
def test_remove_item(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_response

    response = client.get('/delete/1', follow_redirects=True)
    response_text = response.get_data(as_text=True)
    assert 'No recent items completed yet' in response_text 
    assert 'No items in progress' in response_text 