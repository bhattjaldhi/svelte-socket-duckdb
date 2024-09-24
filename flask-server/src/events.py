from flask_socketio import emit
from src.database import update_cell

def register_events(socketio):
    """
    Register SocketIO event handlers.

    This function sets up the SocketIO event listeners for the application.

    Args:
    socketio (SocketIO): The SocketIO instance to register events on.
    """

    @socketio.on('cell_update')
    def handle_cell_update(data):
        """
        Handle the 'cell_update' event.

        This event is triggered when a client requests to update a cell in the database.

        Args:
        data (dict): A dictionary containing the update information.
                     Expected keys: 'row_id', 'column', 'new_value'

        Emits:
        - 'cell_update_broadcast': Broadcast to all clients when update is successful.
        - 'update_failure': Emitted to the requesting client if the update fails.
        """
        # Extract update information from the received data
        row_id = data['row_id']
        column = data['column']
        new_value = data['new_value']

        try:
            # Attempt to update the cell in the database
            # Note: We're accessing the app config through socketio.server.app
            update_cell(socketio.server.app.config['DB_FILE_PATH'], row_id, column, new_value)

            # If successful, broadcast the update to all connected clients
            emit('cell_update_broadcast', data, broadcast=True)

        except Exception as e:
            # If an error occurs during the update, emit a failure event
            # This event is sent only to the client that requested the update
            emit('update_failure', {
                'status': 'failure',
                'error': str(e),
                'row_id': row_id,
                'column': column
            })