from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
    new_sheep = {
        "id": 7,
        "name": "Barbara",
        "breed": "Suffolk",
        "sex": "ewe"
    }
    response = client.post("/sheep", json=new_sheep)
    assert response.status_code == 201
    assert response.json() == new_sheep

    #Check addition to database
    sheep_id = response.json().get("id")
    if sheep_id:
        get_response = client.get(f"/sheep/{sheep_id}")
        assert get_response.status_code == 200
        assert get_response.json() == {**new_sheep, "id": sheep_id}


# --- Extra Credit Tests ---
def test_delete_sheep():
    # Delete an existing sheep
    response = client.delete("/sheep/1")
    assert response.status_code == 204

    # Test deleting a sheep that does not exist.
    response = client.delete("/sheep/200")
    assert response.status_code == 404
    assert response.json() == {"detail": "Sheep not found"}

def test_update_sheep():
    initial_sheep = {
        "id": 8,
        "name": "Darla",
        "breed": "Suffolk",
        "sex": "ewe"
    }
    client.post("/sheep", json=initial_sheep)
    updated_sheep = {
        "id": 8,
        "name": "Daring",
        "breed": "Suffolk",
        "sex": "ram"
    }

    response = client.put("/sheep/8", json=updated_sheep)
    assert response.status_code == 200
    assert response.json() == updated_sheep

    # Test updating a sheep that does not exist
    non_existant_sheep = {
        "id": 201,
        "name": "Smoky",
        "breed": "F1",
        "sex": "ram"
    }
    response = client.put("/sheep/201", json=non_existant_sheep)
    assert response.status_code == 404
    assert response.json() == {"detail": "Sheep with this ID does not exist"}

    # Test mismatched ID in path and Body
    mismatched_sheep = {
        "id": 10,
        "name": "Waddles",
        "breed": "Babydoll",
        "sex": "ewe"
    }
    response = client.put("/sheep/11", json=mismatched_sheep)
    assert response.status_code == 400
    assert response.json() == {"detail": "Ids do not match"}

def test_read_all_sheep():
    response = client.get("/sheep")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(sheep['name'] == "Blondie" for sheep in response.json())
    assert any(sheep['name'] == "Vala" for sheep in response.json())