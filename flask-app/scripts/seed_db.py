import duckdb

def create_tables(conn):
    conn.execute('''
    CREATE TABLE IF NOT EXISTS category (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        amount INTEGER NOT NULL,
        color VARCHAR(40),
        weight REAL,
        category_id INTEGER,
        brand TEXT,
        SKU TEXT NOT NULL,
        country_of_origin VARCHAR(3),
        FOREIGN KEY (category_id) REFERENCES category(id)
    );
    ''')

def seed_data(conn):
    # Seed categories
    categories = [
        (1, 'Electronics'),
        (2, 'Clothing')
    ]
    for category in categories:
        conn.execute("""
        INSERT OR REPLACE INTO category (id, name)
        VALUES (?, ?)
        """, category)

    # Seed products
    products = [
        (1, 'Laptop', 50, 'Silver', 2.5, 1, 'BrandA', 'SKU12345', 'USA'),
        (2, 'T-Shirt', 200, 'Blue', 0.2, 2, None, 'SKU67890', 'CHN')
    ]
    for product in products:
        conn.execute("""
        INSERT OR REPLACE INTO product (id, name, amount, color, weight, category_id, brand, SKU, country_of_origin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, product)

def main():
    conn = duckdb.connect('data/database.db')
    create_tables(conn)
    seed_data(conn)
    conn.close()

if __name__ == '__main__':
    main()