import duckdb
from flask import current_app, abort
from app.models.product import Product, Category


def get_db_connection():
    # Establish and return a connection to the DuckDB database
    return duckdb.connect(current_app.config["DB_FILE_PATH"])


def get_table_data(table_name):
    # Get a database connection
    conn = get_db_connection()

    # Basic validation to prevent SQL injection
    if table_name not in ["product", "category"]:
        abort(400, description="Invalid or missing table name")

    # Execute query to fetch all data from the specified table
    result = conn.execute(f"SELECT * FROM {table_name}").fetchall()

    # Get column names from the query result
    columns = [desc[0] for desc in conn.description]

    # Convert query results to appropriate model instances
    if table_name == "product":
        return [Product(**dict(zip(columns, row))) for row in result]
    elif table_name == "category":
        return [Category(**dict(zip(columns, row))) for row in result]


def update_cell(table_name, row_id, column, new_value):
    # Get a database connection
    conn = get_db_connection()

    # Prepare and execute UPDATE query
    query = f"UPDATE {table_name} SET {column} = ? WHERE id = ?"
    conn.execute(query, [new_value, row_id])

    # Commit the transaction
    conn.commit()
