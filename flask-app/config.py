import os
from dotenv import load_dotenv

# Load the appropriate .env file based on the FLASK_ENV
flask_env = os.environ.get('FLASK_ENV', 'development')
if flask_env == 'testing':
    load_dotenv('.env.test')
else:
    load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'database.db')    
    FLASK_ENV = os.environ.get('FLASK_ENV')

class TestingConfig(Config):
    TESTING = True
    DB_FILE_PATH = os.path.join(os.path.dirname(__file__), 'tests', 'test_database.db')
