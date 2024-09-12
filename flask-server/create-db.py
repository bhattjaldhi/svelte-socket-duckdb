import duckdb

# Define the CSV and database paths
CSV_FILE_PATH = 'data.csv'
DB_FILE_PATH = 'data.db'

# Connect to a DuckDB database file (persistent storage)
con = duckdb.connect(DB_FILE_PATH)

# Load CSV into DuckDB and store it in a table called 'table_data'
con.execute(f"CREATE TABLE table_data AS SELECT * FROM read_csv_auto('{CSV_FILE_PATH}')")

# Verify data has been loaded
result = con.execute("SELECT * FROM table_data").df()
print(result)
