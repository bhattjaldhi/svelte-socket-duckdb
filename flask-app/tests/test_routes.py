def test_get_sheet_product(client, init_database):
    response = client.get("/get-sheet?table=product")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Test Product"


def test_get_sheet_category(client, init_database):
    response = client.get("/get-sheet?table=category")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Test Category"


def test_get_sheet_invalid_table(client):
    response = client.get("/get-sheet?table=invalid")
    assert response.status_code == 400
