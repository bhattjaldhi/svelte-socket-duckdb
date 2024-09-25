from flask_socketio import emit
from app import socketio
from app.services.database import update_cell
from app.models.product import CellUpdateRequest, CellUpdateResponse, UpdateFailureResponse
from pydantic import ValidationError

@socketio.on('cell_update')
def handle_cell_update(data):
    try:
        update_request = CellUpdateRequest(**data)
        update_cell(
            update_request.table_name,
            update_request.row_id,
            update_request.column,
            update_request.new_value
        )
        response = CellUpdateResponse(status="success", message="Cell updated successfully")
        emit('cell_update_broadcast', response.dict(), broadcast=True)
    except ValidationError as ve:
        failure_response = UpdateFailureResponse(
            status="failure",
            error="Validation error: " + str(ve),
            row_id=data.get('row_id'),
            column=data.get('column')
        )
        emit('update_failure', failure_response.dict())
    except Exception as e:
        failure_response = UpdateFailureResponse(
            status="failure",
            error=str(e),
            row_id=data.get('row_id'),
            column=data.get('column')
        )
        emit('update_failure', failure_response.dict())