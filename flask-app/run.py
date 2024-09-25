from app import create_app, socketio

# def initialize_database():
#     from scripts.seed_db import main as seed_main
#     seed_main()

app = create_app()

print(__name__)
if __name__ == '__main__':
   socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0', port=5000)