import duckdb

def get_all_data(db_path):
    """
    Retrieve all data from the table_data table in the DuckDB database.

    Args:
    db_path (str): The file path to the DuckDB database.

    Returns:
    list: A list of dictionaries, where each dictionary represents a row in the table.
    """
    # Connect to the DuckDB database
    con = duckdb.connect(db_path)
    
    # SQL query to select all data from the table
    query = "SELECT * FROM table_data"
    
    # Execute the query and convert the result to a pandas DataFrame
    result = con.execute(query).df()
    
    # Convert the DataFrame to a list of dictionaries
    return result.to_dict(orient='records')

def update_cell(db_path, row_id, column, new_value):
    """
    Update a specific cell in the table_data table of the DuckDB database.

    Args:
    db_path (str): The file path to the DuckDB database.
    row_id (int): The ID of the row to update.
    column (str): The name of the column to update.
    new_value (any): The new value to set in the specified cell.

    Note:
    This function does not return any value. It will raise an exception if the update fails.
    """
    # Connect to the DuckDB database
    con = duckdb.connect(db_path)
    
    # Prepare the SQL update query
    # Note: The column name is inserted directly into the query string.
    # This is generally unsafe and could lead to SQL injection if 'column' comes from user input.
    # In a production environment, you should use a safer method to handle dynamic column names.
    update_query = f"UPDATE table_data SET {column} = ? WHERE id = ?"
    
    # Execute the update query with the provided values
    con.execute(update_query, [new_value, row_id])