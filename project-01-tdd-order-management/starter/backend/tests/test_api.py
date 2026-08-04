import pytest
from backend.app import app, in_memory_storage

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    in_memory_storage.clear()
    with app.test_client() as client:
        yield client

def test_add_order_api_success(client):
    order_data = {
        "order_id": "API001", "item_name": "API Laptop", "quantity": 1, "customer_id": "APICUST001"
    }
    response = client.post('/api/orders', json=order_data)
    assert response.status_code == 201
    assert response.json['order_id'] == "API001"

def test_get_order_api_success(client):
    client.post('/api/orders', json={
        "order_id": "GET001", "item_name": "Test Item", "quantity": 1, "customer_id": "C1"
    })
    response = client.get('/api/orders/GET001')
    assert response.status_code == 200
    assert response.json['order_id'] == "GET001"

def test_get_order_api_not_found(client):
    response = client.get('/api/orders/NONEXISTENT')
    assert response.status_code == 404

def test_update_order_status_api_success(client):
    client.post('/api/orders', json={
        "order_id": "UPDATE001", "item_name": "Test Item", "quantity": 1, "customer_id": "C1"
    })
    response = client.put('/api/orders/UPDATE001/status', json={"new_status": "shipped"})
    assert response.status_code == 200
    assert response.json['status'] == "shipped"

def test_list_all_orders_api_with_data(client):
    client.post('/api/orders', json={"order_id": "LST001", "item_name": "Item A", "quantity": 1, "customer_id": "C1"})
    client.post('/api/orders', json={"order_id": "LST002", "item_name": "Item B", "quantity": 2, "customer_id": "C2"})
    response = client.get('/api/orders')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_list_orders_by_status_api_matching(client):
    client.post('/api/orders', json={"order_id": "S001", "item_name": "A", "quantity": 1, "customer_id": "C1", "status": "pending"})
    client.post('/api/orders', json={"order_id": "S002", "item_name": "B", "quantity": 2, "customer_id": "C2", "status": "shipped"})
    response = client.get('/api/orders?status=pending')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['order_id'] == "S001"


def test_add_order_api_rejects_invalid_payload(client):
    response = client.post('/api/orders', json={
        "order_id": "BAD001", "item_name": "Item", "quantity": 0, "customer_id": "C1"
    })

    assert response.status_code == 400
    assert "positive integer" in response.json["error"]


def test_add_order_api_rejects_duplicate_id(client):
    order = {"order_id": "DUP001", "item_name": "Item", "quantity": 1, "customer_id": "C1"}
    client.post('/api/orders', json=order)

    response = client.post('/api/orders', json=order)

    assert response.status_code == 409


def test_update_order_status_at_restful_endpoint(client):
    client.post('/api/orders', json={
        "order_id": "STATUS001", "item_name": "Item", "quantity": 1, "customer_id": "C1"
    })

    response = client.put('/api/orders/STATUS001', json={"new_status": "delivered"})

    assert response.status_code == 200
    assert response.json["status"] == "delivered"


def test_update_order_status_api_rejects_unknown_status(client):
    client.post('/api/orders', json={
        "order_id": "STATUS001", "item_name": "Item", "quantity": 1, "customer_id": "C1"
    })

    response = client.put('/api/orders/STATUS001', json={"new_status": "unknown"})

    assert response.status_code == 400


def test_update_order_status_api_returns_not_found(client):
    response = client.put('/api/orders/MISSING', json={"new_status": "shipped"})

    assert response.status_code == 404
