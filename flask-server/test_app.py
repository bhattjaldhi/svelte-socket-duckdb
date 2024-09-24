# test_app.py

import pytest
from flask import json
from app import create_app
import duckdb
from src.config import TestConfig

# Define the path for the test database
DB_FILE_PATH = 'test_data.db'

@pytest.fixture
def app():
    # Create a test Flask application with SocketIO
    app, socketio = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    # Create a test client for the Flask application
    return app.test_client()

@pytest.fixture
def socketio_client(app):
    # Create a SocketIO test client
    return app.extensions['socketio'].test_client(app)

@pytest.fixture
def init_database(app):
    # Initialize the test database with sample data
    with app.app_context():
        con = duckdb.connect(app.config['DB_FILE_PATH'])
        # Create a table and insert test data
        con.execute("CREATE TABLE IF NOT EXISTS table_data (id INTEGER, name VARCHAR, value INTEGER)")
        con.execute("INSERT INTO table_data VALUES (1, 'Test', 100)")
        yield con
        # Clean up the database after the test
        con.execute("DROP TABLE IF EXISTS table_data")
        con.close()

def test_main_route(client):
    # Test the main route of the application
    response = client.get('/')
    assert response.status_code == 200
    assert b'Successfully loaded.' in response.data

def test_get_table_data(client, init_database):
    # Test retrieving table data from the API
    response = client.get('/api/table')
    assert response.status_code == 200
    data = json.loads(response.data)
    # Check if the retrieved data matches the inserted test data
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Test'
    assert data[0]['value'] == 100

def test_cell_update(app, client, socketio_client, init_database):
    # Test updating a cell via SocketIO
    socketio_client.emit('cell_update', {'row_id': 1, 'column': 'value', 'new_value': 200})
    received = socketio_client.get_received()
    # Check if the update was broadcasted correctly
    assert len(received) == 1
    assert received[0]['name'] == 'update_failure'
    assert received[0]['args'][0]['row_id'] == 1
    assert received[0]['args'][0]['column'] == 'value'
    assert received[0]['args'][0]['new_value'] == 200

    # Verify the update in the database
    with app.app_context():
        con = duckdb.connect(client.application.config['DB_FILE_PATH'])
        result = con.execute("SELECT value FROM table_data WHERE id = 1").fetchone()
        assert result[0] == 200

def test_cell_update_invalid_data(socketio_client, init_database):
    # Test updating a cell with invalid data
    socketio_client.emit('cell_update', {'row_id': 999, 'column': 'nonexistent', 'new_value': 'invalid'})
    received = socketio_client.get_received()
    # Check if the update failure was handled correctly
    assert len(received) == 1
    assert received[0]['name'] == 'update_failure'
    assert 'error' in received[0]['args'][0]

def test_get_table_data_empty(client, init_database):
    # Test retrieving data from an empty table
    with client.application.app_context():
        con = duckdb.connect(client.application.config['DB_FILE_PATH'])
        con.execute("DELETE FROM table_data")
    
    response = client.get('/api/table')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0

def test_get_table_data_error(client):
    # Test error handling when the database file doesn't exist
    client.application.config['DB_FILE_PATH'] = 'nonexistent.db'
    response = client.get('/api/table')
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data