import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS'))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    SECRET_KEY= os.getenv('SECRET_KEY')