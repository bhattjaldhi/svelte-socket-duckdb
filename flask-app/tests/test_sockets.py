import pytest
from flask_socketio import SocketIOTestClient

@pytest.fixture
def socket_client(app, init_database):
    from app import socketio
    return SocketIOTestClient(app, socketio)

def test_cell_update(socket_client):
    socket_client.emit('cell_update', {
        'table_name': 'product',
        'row_id': 1,
        'column': 'amount',
        'new_value': '20'
    })
    received = socket_client.get_received()
    assert len(received) == 1
    assert received[0]['name'] == 'cell_update_broadcast'
    assert received[0]['args'][0]['status'] == 'success'

def test_cell_update_invalid_data(socket_client):
    socket_client.emit('cell_update', {
        'table_name': 'invalid_table',
        'row_id': 1,
        'column': 'amount',
        'new_value': '20'
    })
    received = socket_client.get_received()
    assert len(received) == 1
    assert received[0]['name'] == 'update_failure'
    assert received[0]['args'][0]['status'] == 'failure'
    assert 'error' in received[0]['args'][0]