from flask import jsonify, request, abort
from flask_pydantic import validate
from . import main_bp
from app.services.database import get_table_data
from app.models.product import ProductResponse

@main_bp.route('/get-sheet')
@validate()
def get_table():
    # Extract the table name from the query parameters
    table_name = request.args.get('table')
    
    # Validate that the table name is provided and is allowed
    if not table_name or table_name not in ["product", "category"]:
        abort(400, description="Invalid or missing table name")
    
    # Fetch data from the specified table
    data = get_table_data(table_name)
    
    # Wrap the data in a ProductResponse model and return as JSON
    return jsonify(ProductResponse(data=data).dict())