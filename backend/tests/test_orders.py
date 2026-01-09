import pytest
from fastapi import status


@pytest.fixture
def category(client):
    response = client.post(
        "/api/v1/categories/",
        json={"name": "Eletrônicos", "description": "Produtos eletrônicos"}
    )
    return response.json()


@pytest.fixture
def supplier(client):
    response = client.post(
        "/api/v1/suppliers/",
        json={
            "name": "Fornecedor ABC",
            "contact_email": "contato@abc.com"
        }
    )
    return response.json()


@pytest.fixture
def product(client, category, supplier):
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "Notebook",
            "sku": "NB-001",
            "price": 2500.00,
            "stock_quantity": 10,
            "category_id": category["id"],
            "supplier_id": supplier["id"]
        }
    )
    return response.json()


def test_create_order(client):
    response = client.post(
        "/api/v1/orders/",
        json={"total_value": 100.00}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["total_value"] == 100.00
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data


def test_get_order(client):
    create_response = client.post(
        "/api/v1/orders/",
        json={"total_value": 100.00}
    )
    order_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == order_id
    assert data["total_value"] == 100.00


def test_get_all_orders(client):
    client.post("/api/v1/orders/", json={"total_value": 100.00})
    client.post("/api/v1/orders/", json={"total_value": 200.00})
    
    response = client.get("/api/v1/orders/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_update_order(client):
    create_response = client.post(
        "/api/v1/orders/",
        json={"total_value": 100.00}
    )
    order_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/v1/orders/{order_id}",
        json={"status": "processing", "total_value": 150.00}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "processing"
    assert data["total_value"] == 150.00


def test_add_item_to_order(client, product):
    order_response = client.post(
        "/api/v1/orders/",
        json={"total_value": 0.00}
    )
    order_id = order_response.json()["id"]
    
    response = client.post(
        f"/api/v1/orders/{order_id}/items",
        json={
            "product_id": product["id"],
            "quantity": 2,
            "price": 2500.00
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["product_id"] == product["id"]
    assert data["quantity"] == 2
    assert data["price"] == 2500.00
    assert "id" in data
    
    order_response = client.get(f"/api/v1/orders/{order_id}")
    order_data = order_response.json()
    assert order_data["total_value"] == 5000.00


def test_add_item_to_order_insufficient_stock(client, product):
    order_response = client.post(
        "/api/v1/orders/",
        json={"total_value": 0.00}
    )
    order_id = order_response.json()["id"]
    
    response = client.post(
        f"/api/v1/orders/{order_id}/items",
        json={
            "product_id": product["id"],
            "quantity": 100,
            "price": 2500.00
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_remove_item_from_order(client, product):
    order_response = client.post(
        "/api/v1/orders/",
        json={"total_value": 0.00}
    )
    order_id = order_response.json()["id"]
    
    item_response = client.post(
        f"/api/v1/orders/{order_id}/items",
        json={
            "product_id": product["id"],
            "quantity": 2,
            "price": 2500.00
        }
    )
    item_id = item_response.json()["id"]
    
    response = client.delete(f"/api/v1/orders/{order_id}/items/{item_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    order_response = client.get(f"/api/v1/orders/{order_id}")
    order_data = order_response.json()
    assert order_data["total_value"] == 0.00


def test_complete_order(client, product):
    order_response = client.post(
        "/api/v1/orders/",
        json={"total_value": 0.00}
    )
    order_id = order_response.json()["id"]
    
    client.post(
        f"/api/v1/orders/{order_id}/items",
        json={
            "product_id": product["id"],
            "quantity": 2,
            "price": 2500.00
        }
    )
    
    response = client.post(f"/api/v1/orders/{order_id}/complete")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "completed"
    
    product_response = client.get(f"/api/v1/products/{product['id']}")
    product_data = product_response.json()
    assert product_data["stock_quantity"] == 8


def test_delete_order(client):
    create_response = client.post(
        "/api/v1/orders/",
        json={"total_value": 100.00}
    )
    order_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/orders/{order_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/api/v1/orders/{order_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

