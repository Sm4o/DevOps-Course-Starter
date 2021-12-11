import os


class Config:
    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.DB_CONNECTION = os.environ.get('DB_CONNECTION')
        self.DATABASE_NAME = os.environ.get('DATABASE_NAME')

        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
