import os
import time
from threading import Thread

import pytest
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
import pymongo

from todo_app import app


@pytest.fixture(scope='module', autouse=True)
def app_with_temp_database():
    # Remove if it causes issues with Travis environment variables
    # Loading environment variables 
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    os.environ['DATABASE_NAME'] += '_test'

    # Construct the new application
    application = app.create_app() 
    application.config['LOGIN_DISABLED'] = True

    # Start the app in its own thread.
    thread = Thread(target = lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)

    # Drop test database
    mongo_client = pymongo.MongoClient(os.environ.get("DB_CONNECTION"))
    mongo_client.drop_database(os.environ['DATABASE_NAME'])


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver


def test_task_journey(driver):
    # Waiting for application to be ready for use due to lag
    time.sleep(3)

    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App' 


def test_create_task(driver):
    time.sleep(3)

    title_element = driver.find_element_by_id('title')
    title_element.send_keys("Title E2E Test")

    description_element = driver.find_element_by_id('description')
    description_element.send_keys("Description E2E Test")

    description_element.submit()

    time.sleep(3)

    assert "Title E2E Test" in driver.page_source
    assert "Description E2E Test" in driver.page_source


def test_complete_task(driver):
    time.sleep(3)

    doing_button = driver.find_element_by_xpath("//a[contains(text(), 'Mark as Doing')]")
    doing_button.click()
    time.sleep(6)

    done_button = driver.find_element_by_xpath("//a[contains(text(), 'Mark as Done')]")
    done_button.click()
    time.sleep(6)

    assert "Title E2E Test" in driver.page_source
    assert "Description E2E Test" in driver.page_source
