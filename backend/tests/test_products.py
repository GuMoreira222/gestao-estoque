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


def test_create_product(client, category, supplier):
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
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Notebook"
    assert data["sku"] == "NB-001"
    assert data["price"] == 2500.00
    assert data["stock_quantity"] == 10
    assert "id" in data


def test_create_product_duplicate_sku(client, category, supplier):
    client.post(
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
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "Outro Notebook",
            "sku": "NB-001",
            "price": 3000.00,
            "stock_quantity": 5,
            "category_id": category["id"],
            "supplier_id": supplier["id"]
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_product_invalid_category(client, supplier):
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "Notebook",
            "sku": "NB-001",
            "price": 2500.00,
            "stock_quantity": 10,
            "category_id": 999,
            "supplier_id": supplier["id"]
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_product_invalid_supplier(client, category):
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "Notebook",
            "sku": "NB-001",
            "price": 2500.00,
            "stock_quantity": 10,
            "category_id": category["id"],
            "supplier_id": 999
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_product(client, category, supplier):
    create_response = client.post(
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
    product_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Notebook"


def test_get_all_products(client, category, supplier):
    client.post(
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
    client.post(
        "/api/v1/products/",
        json={
            "name": "Mouse",
            "sku": "MS-001",
            "price": 50.00,
            "stock_quantity": 20,
            "category_id": category["id"],
            "supplier_id": supplier["id"]
        }
    )
    
    response = client.get("/api/v1/products/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_update_product(client, category, supplier):
    create_response = client.post(
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
    product_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/v1/products/{product_id}",
        json={"name": "Notebook Atualizado", "price": 2700.00}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Notebook Atualizado"
    assert data["price"] == 2700.00


def test_delete_product(client, category, supplier):
    create_response = client.post(
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
    product_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

