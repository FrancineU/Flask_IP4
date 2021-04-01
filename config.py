import os
class Config:
    '''
    General configuration parent class
    '''
    QUOTE_API_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOADED_PHOTOS_DEST = 'app/static/photos'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sarah:123@localhost/blog'

class DevConfig(Config):
    '''
    Development configuration child class

    Args:
        Config: The parent configuration class with general configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sarah:123@localhost/blog'
    DEBUG = True

class ProdConfig(Config):
    '''
    Production configuration child class

    Args: 
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

config_options = {
    'development' : DevConfig,
    'production' : ProdConfig,
    'test' : TestConfig
}