from flask import Flask
from flask_socketio import SocketIO

# Initialize SocketIO without app
socketio = SocketIO()


def create_app(config_name="default"):
    # Create Flask app instance
    app = Flask(__name__)

    # Load config based on environment
    if config_name == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.Config")

    # Register main blueprint
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # Initialize SocketIO with app
    socketio.init_app(app)

    return app
