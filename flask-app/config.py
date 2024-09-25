import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    DB_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'database.db')

class TestingConfig(Config):
    TESTING = True
    DB_FILE_PATH = os.path.join(os.path.dirname(__file__), 'tests', 'testdatabase.db')  # Use in-memory database for testing