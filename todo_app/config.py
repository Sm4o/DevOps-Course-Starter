import os


class TrelloConfig:
    """ Configuration variables for Trello API """
    def __init__(self):
        self.BOARD_ID = os.environ.get('BOARD_ID')
        self.APP_KEY = os.environ.get('APP_KEY')
        self.TOKEN = os.environ.get('TOKEN')