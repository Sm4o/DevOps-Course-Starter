import os


class Config:
    """Base configuration variables."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")


class TrelloConfig:
    """ Configuration variables for Trello API """
    BOARD_ID = os.environ.get('BOARD_ID')
    APP_KEY = os.environ.get('APP_KEY')
    TOKEN = os.environ.get('TOKEN')