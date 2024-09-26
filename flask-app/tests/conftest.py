import pytest
from app import create_app
from app.services.database import get_db_connection


@pytest.fixture
def app():
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    with app.app_context():
        conn = get_db_connection()
        yield conn
        conn.close()


@pytest.fixture
def init_database(db):
    # Create tables and insert test data
    db.execute(
        """
    CREATE TABLE IF NOT EXISTS category (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    """
    )
    db.execute(
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
    db.execute("INSERT INTO category (id, name) VALUES (1, 'Test Category');")
    db.execute(
        """
        INSERT INTO product (
            id, name, amount, color, weight,
            category_id, brand, SKU, country_of_origin
        ) VALUES (
            1, 'Test Product', 10, 'Red', 1.5,
            1, 'Test Brand', 'TST123', 'USA'
        );
        """
    )
    db.commit()

    yield db

    # Clean up
    db.execute("DROP TABLE IF EXISTS product;")
    db.execute("DROP TABLE IF EXISTS category;")
    db.commit()
