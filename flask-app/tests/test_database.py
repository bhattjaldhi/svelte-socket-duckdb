import pytest
from app.services.database import get_table_data, update_cell

@pytest.mark.usefixtures("init_database")
def test_get_table_data(app):
    with app.app_context():
        data = get_table_data('product')
        assert len(data) == 1
        assert data[0].name == 'Test Product'

@pytest.mark.usefixtures("init_database")
def test_update_cell(app):
    with app.app_context():
        update_cell('product', 1, 'amount', 20)
        data = get_table_data('product')
        assert data[0].amount == 20