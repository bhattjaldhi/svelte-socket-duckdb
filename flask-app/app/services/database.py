import duckdb
from flask import current_app, abort
import threading
from app.models.product import Product, Category
from celery import shared_task
from contextlib import contextmanager
from typing import List, Dict, Any
import os


class DuckDBSingleton:
    _instance = None
    _connection = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.db_path = self.get_db_path()
        self._connection = None

    @staticmethod
    def get_db_path() -> str:
        try:
            return current_app.config["DB_FILE_PATH"]
        except RuntimeError:
            return os.environ.get("DB_FILE_PATH", "/app/data/database.db")

    def get_connection(self, write: bool = False) -> duckdb.DuckDBPyConnection:
        access_mode = "READ_WRITE" if write else "READ_ONLY"
        if self._connection is None:
            self._connection = duckdb.connect(
                f"{self.db_path}?access_mode={access_mode}"
            )
        return self._connection

    def close_connection(self):
        with self._lock:
            if self._connection:
                self._connection.close()
                self._connection = None


@contextmanager
def get_db_connection(write: bool = False):
    db_manager = DuckDBSingleton.get_instance()
    conn = db_manager.get_connection(write)
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        if write:
            conn.commit()


@shared_task
def get_table_data(table_name: str) -> List[Dict[str, Any]]:
    if table_name not in ["product", "category"]:
        abort(400, description="Invalid table name")

    with get_db_connection() as conn:
        result = conn.execute(f"SELECT * FROM {table_name}").fetchall()
        columns = [desc[0] for desc in conn.description]

    if table_name == "product":
        return [Product(**dict(zip(columns, row))).dict() for row in result]
    elif table_name == "category":
        return [Category(**dict(zip(columns, row))).dict() for row in result]


@shared_task
def update_cell(
    table_name: str, row_id: int, column: str, new_value: Any
) -> Dict[str, str]:
    if table_name not in ["product", "category"]:
        return {"status": "error", "message": "Invalid table name"}

    try:
        with get_db_connection(write=True) as conn:
            query = f"UPDATE {table_name} SET {column} = ? WHERE id = ?"
            conn.execute(query, [new_value, row_id])
        return {"status": "success", "message": "Cell updated successfully"}
    except duckdb.Error as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


def get_table_data_sync(table_name: str) -> List[Dict[str, Any]]:
    return get_table_data.delay(table_name).get()


def update_cell_sync(
    table_name: str, row_id: int, column: str, new_value: Any
) -> Dict[str, str]:
    return update_cell.delay(table_name, row_id, column, new_value).get()
