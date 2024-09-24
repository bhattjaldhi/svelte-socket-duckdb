from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from src.config import Config
from src.routes import register_routes
from src.events import register_events
import logging

# Initialize these variables in the global scope
app = None
socketio = None

def create_app(config_class=Config):
    global app, socketio
    
    # Initialize the Flask application
    app = Flask(__name__)
    
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Load configuration from the provided config class
    app.config.from_object(config_class)

    # Enable CORS for all routes and origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize SocketIO with the app
    if app.config.get('TESTING', False):
        # Configuration for testing mode
        socketio = SocketIO(app, 
                            cors_allowed_origins="*",
                            async_mode=None,
                            message_queue=None)
        app.logger.debug("SocketIO initialized in testing mode")
    else:
        # Configuration for non-testing mode
        socketio = SocketIO(app, 
                            cors_allowed_origins="*",
                            async_mode='eventlet',
                            message_queue='redis://redis-main:6379')
        app.logger.debug("SocketIO initialized in production mode")

    # Register HTTP routes
    register_routes(app)
    
    # Register SocketIO event handlers
    register_events(socketio)

    return app, socketio

# Create the Flask app and SocketIO instance
app, socketio = create_app()

if __name__ == '__main__':
    # This block only executes if the script is run directly (not imported)
    
    # Run the app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)