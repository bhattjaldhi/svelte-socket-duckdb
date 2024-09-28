from flask import Flask
from flask_socketio import SocketIO
from app.services.database import DuckDBSingleton
from .celery import make_celery, celery

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

    # Configure Celery
    celery.conf.update(app.config)
    app.celery = make_celery(app)

    # Register main blueprint
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # Initialize SocketIO with app
    socketio.init_app(app)

    # Close duckdb connection when app is shutdown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_instance = DuckDBSingleton.get_instance()
        if db_instance:
            db_instance.close_connection()

    return app
