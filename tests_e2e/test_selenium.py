import os
import time
from threading import Thread

import pytest
import requests
from dotenv import find_dotenv, load_dotenv
from requests.api import delete
from selenium import webdriver


# Loading environment variables 
file_path = find_dotenv('.env')
load_dotenv(file_path, override=True)

BASE_URL = "https://api.trello.com/1/"
API_KEY = os.environ.get('APP_KEY')
TOKEN = os.environ.get('TOKEN')


def create_trello_board():
    endpoint = 'boards'
    params = {
        'key': API_KEY,
        'token': TOKEN,
        'name': "Corndel ToDo-List App E2E Tests",
    }
    response = requests.post(BASE_URL + endpoint, params=params)
    json_response = response.json()
    board_id = json_response['id']
    return board_id


def delete_trello_board(board_id):
    endpoint = f'boards/{board_id}'
    params = {
        'key': API_KEY,
        'token': TOKEN,
    }
    requests.delete(BASE_URL + endpoint, params=params)


@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['BOARD_ID'] = board_id

    # Construct the new application
    from todo_app import app  # FIXME: I was forced to import here, otherwise loads with old BOARD_ID
    application = app.create_app() 

    # Start the app in its own thread.
    thread = Thread(target = lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    delete_trello_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    # Waiting for application to be ready for use due to lag
    time.sleep(3)

    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App' 


def test_create_task(driver, app_with_temp_board):
    time.sleep(3)

    title_element = driver.find_element_by_id('title')
    title_element.send_keys("Title E2E Test")

    description_element = driver.find_element_by_id('description')
    description_element.send_keys("Description E2E Test")

    description_element.submit()

    time.sleep(3)

    assert "Title E2E Test" in driver.page_source
    assert "Description E2E Test" in driver.page_source


def test_complete_task(driver, app_with_temp_board):
    time.sleep(3)

    done_button = driver.find_element_by_xpath("//a[contains(text(), 'Mark as Doing')]")
    done_button.click()

    time.sleep(3)

    done_button = driver.find_element_by_xpath("//a[contains(text(), 'Mark as Done')]")
    done_button.click()

    assert "Title E2E Test" in driver.page_source
    assert "Description E2E Test" in driver.page_source


def test_delete_task(driver, app_with_temp_board):
    time.sleep(3)

    delete_button = driver.find_element_by_xpath("//a[contains(text(), 'Delete')]")
    delete_button.click()

    time.sleep(3)

    assert "Title E2E Test" not in driver.page_source
    assert "Description E2E Test" not in driver.page_source
