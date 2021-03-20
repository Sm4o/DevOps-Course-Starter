import os

import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = "https://api.trello.com/1/"
BOARD_ID = os.getenv('BOARD_ID')


def get_board_cards():
    endpoint = f"boards/{BOARD_ID}/cards"
    params = {
        'key': os.getenv('APP_KEY'),
        'token': os.getenv('TOKEN'),
    }
    resp = requests.get(BASE_URL + endpoint, params=params)
    return resp.json()


def get_board_lists():
    endpoint = f"boards/{BOARD_ID}/lists"
    params = {
        'key': os.getenv('APP_KEY'),
        'token': os.getenv('TOKEN'),
    }
    resp = requests.get(BASE_URL + endpoint, params=params)
    return resp.json()


def create_card(name):
    endpoint = "cards"
    lists = get_board_lists()
    todo_list = next((list for list in lists if list['name'] == 'To Do'), None)
    params = {
        'key': os.getenv('APP_KEY'),
        'token': os.getenv('TOKEN'),
        'name': name,
        'idList': todo_list['id'],
    }
    resp = requests.post(BASE_URL + endpoint, params=params)
    return resp.json()    


def delete_card(card_id):
    endpoint = f"cards/{card_id}"
    params = {
        'key': os.getenv('APP_KEY'),
        'token': os.getenv('TOKEN'),
    }
    resp = requests.delete(BASE_URL + endpoint, params=params)
    print(resp.text)


def mark_card_as_done(card_id):
    endpoint = f"cards/{card_id}"
    lists = get_board_lists()
    done_list = next((list for list in lists if list['name'] == 'Done'), None)
    params = {
        'key': os.getenv('APP_KEY'),
        'token': os.getenv('TOKEN'),
        'id': card_id,
        'idList': done_list['id'],
    }
    resp = requests.put(BASE_URL + endpoint, params=params)
    print(resp.json())
