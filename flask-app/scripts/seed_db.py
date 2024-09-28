from ..app.services.database import get_db_connection


def create_tables():
    try:
        with get_db_connection(write=True) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS category (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                );
                """
            )

            conn.execute(
                """
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
                """
            )
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")


def seed_data():
    try:
        with get_db_connection(write=True) as conn:
            # Seed categories
            categories = [(1, "Electronics"), (2, "Clothing")]
            for category in categories:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO category (id, name)
                    VALUES (?, ?)
                    """,
                    category,
                )

            # Seed products
            products = [
                (1, "Laptop", 50, "Silver", 2.5, 1, "BrandA", "SKU12345", "USA"),
                (2, "T-Shirt", 200, "Blue", 0.2, 2, None, "SKU67890", "CHN"),
            ]
            for product in products:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO product (
                        id, name, amount, color, weight,
                        category_id, brand, SKU, country_of_origin
                    ) VALUES (
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?
                    )
                    """,
                    product,
                )
        print("Data seeded successfully.")
    except Exception as e:
        print(f"Error seeding data: {e}")


def main():
    create_tables()
    seed_data()


if __name__ == "__main__":
    main()
