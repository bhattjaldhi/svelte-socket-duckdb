# app.py

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import duckdb

def create_app(db_path='data.db', testing=False):
    # Create and configure the Flask application
    app = Flask(__name__)
    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Configure SocketIO based on whether we're testing or not
    if not testing:
        # For production: use eventlet and Redis message queue
        socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', message_queue='redis://redis-main:6379')
    else:
        # For testing: don't use message queue
        socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)

    # Set the database file path in the app configuration
    app.config['DB_FILE_PATH'] = db_path

    @app.route("/", methods=['GET'])
    def main():
        # Root route to check if the application is running
        return 'Successfully loaded.'

    @app.route('/api/table', methods=['GET'])
    def get_table_data():
        # Route to fetch all data from the table
        try:
            # Connect to the DuckDB database
            con = duckdb.connect(app.config['DB_FILE_PATH'])
            # Execute query to select all data
            query = "SELECT * FROM table_data"
            result = con.execute(query).df()
            # Convert result to dictionary for JSON serialization
            data = result.to_dict(orient='records')
            return jsonify(data), 200
        except Exception as e:
            # Return error message if something goes wrong
            return jsonify({'error': str(e)}), 500

    @socketio.on('cell_update')
    def handle_cell_update(data):
        # SocketIO event handler for updating a cell
        row_id = data['row_id']
        column = data['column']
        new_value = data['new_value']
        try:
            # Connect to the DuckDB database
            con = duckdb.connect(app.config['DB_FILE_PATH'])
            # Execute update query
            update_query = f"UPDATE table_data SET {column} = ? WHERE id = ?"
            con.execute(update_query, [new_value, row_id])
            # Broadcast the update to all connected clients
            emit('cell_update_broadcast', data, broadcast=True)
        except Exception as e:
            # Emit error message if update fails
            emit('update_failure', {'status': 'failure', 'error': str(e), 'row_id': row_id, 'column': column})

    return app, socketio

if __name__ == '__main__':
    # Create the app and run it when this script is executed directly
    app, socketio = create_app()
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)