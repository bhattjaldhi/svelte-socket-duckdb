import duckdb
from flask import current_app
from app.models.product import Product, Category
from flask import abort

def get_db_connection():
    return duckdb.connect(current_app.config['DB_FILE_PATH'])

def get_table_data(table_name):
    conn = get_db_connection()
    
    # Basic validation to prevent SQL injection
    if table_name not in ["product", "category"]:
        abort(400, description="Invalid or missing table name")
    
    result = conn.execute(f"SELECT * FROM {table_name}").fetchall()
    columns = [desc[0] for desc in conn.description]
    
    if table_name == "product":
        return [Product(**dict(zip(columns, row))) for row in result]
    elif table_name == "category":
        return [Category(**dict(zip(columns, row))) for row in result]

def update_cell(table_name, row_id, column, new_value):
    conn = get_db_connection()
    query = f"UPDATE {table_name} SET {column} = ? WHERE id = ?"
    conn.execute(query, [new_value, row_id])
    conn.commit()