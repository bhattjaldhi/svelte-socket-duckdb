class Config:
    """
    Base configuration class for the application.
    """
    
    # Flag to indicate whether the application is in testing mode
    TESTING = False
    
    # Path to the database file
    # In production, this will use 'data.db'
    DB_FILE_PATH = 'data.db'

class TestConfig(Config):
    """
    Configuration class for testing environment.
    
    This class inherits from the base Config class and
    overrides settings specific to the testing environment.
    """
    
    # Set TESTING to True for the testing environment
    # This can trigger different behaviors in the application
    # (e.g., disabling certain features, using mock services)
    TESTING = True
    
    # Use a separate database file for testing
    # This ensures tests don't interfere with the production database
    DB_FILE_PATH = 'test_data.db'