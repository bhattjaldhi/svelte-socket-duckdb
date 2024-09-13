
import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import duckdb


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for REST API
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', message_queue='redis://haproxy:6379/0')  # Allow CORS for WebSocket

# Path to the DuckDB .db file
DB_FILE_PATH = 'data.db'

@app.route('/table', methods=['GET'])
def get_table_data():
    try:
        # Connect to the DuckDB .db file
        con = duckdb.connect(DB_FILE_PATH)

        # Execute a query to get all data from the table
        query = "SELECT * FROM table_data"
        result = con.execute(query).df()

        # Convert the DuckDB result to a list of dictionaries for JSON serialization
        data = result.to_dict(orient='records')

        # Return the data as JSON
        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# WebSocket handler to listen for cell updates
@socketio.on('cell_update')
def handle_cell_update(data):
    row_id = data['row_id']
    column = data['column']
    new_value = data['new_value']

    try:
        # Connect to the DuckDB database
        con = duckdb.connect(DB_FILE_PATH)

        # Update the specific cell in the DuckDB table
        update_query = f"UPDATE table_data SET {column} = ? WHERE id = ?"
        con.execute(update_query, [new_value, row_id])

        # Broadcast the update to all clients
        emit('cell_update_broadcast', data, broadcast=True)

    except Exception as e:
        emit('update_failure', {'status': 'failure', 'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
