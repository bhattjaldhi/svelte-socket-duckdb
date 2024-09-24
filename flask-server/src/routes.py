from flask import jsonify
from src.database import get_all_data

def register_routes(app):
    """
    Register HTTP routes for the Flask application.

    This function defines and attaches all the route handlers to the given Flask app.

    Args:
    app (Flask): The Flask application instance.
    """

    @app.route("/", methods=['GET'])
    def main():
        """
        Route handler for the root URL ('/').

        This route serves as a simple check to verify if the application is running.

        Returns:
        str: A simple string message indicating successful loading.
        """
        return 'Successfully loaded.'

    @app.route('/api/table', methods=['GET'])
    def get_table_data():
        """
        Route handler for fetching all data from the table.

        This route retrieves all records from the database and returns them as JSON.

        Returns:
        tuple: A tuple containing:
               - JSON response with the data or error message
               - HTTP status code (200 for success, 500 for server error)

        Note:
        The actual database operation is performed by the get_all_data function
        from the database module.
        """
        try:
            # Attempt to retrieve all data from the database
            data = get_all_data(app.config['DB_FILE_PATH'])
            
            # If successful, return the data as JSON with a 200 status code
            return jsonify(data), 200
        
        except Exception as e:
            # If an error occurs, return a JSON object with the error message
            # and a 500 (Internal Server Error) status code
            return jsonify({'error': str(e)}), 500