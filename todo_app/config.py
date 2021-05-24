import os

class TrelloConfig:
    """ Configuration variables for Trello API """
    BOARD_ID = os.environ.get('BOARD_ID')
    APP_KEY = os.environ.get('APP_KEY')
    TOKEN = os.environ.get('TOKEN')