from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.Config')
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    socketio.init_app(app)
    
    return app