import pytest
from fastapi import status


def test_create_supplier(client):
    response = client.post(
        "/api/v1/suppliers/",
        json={
            "name": "Fornecedor ABC",
            "contact_email": "contato@abc.com",
            "cnpj": "12.345.678/0001-90"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Fornecedor ABC"
    assert data["contact_email"] == "contato@abc.com"
    assert "id" in data


def test_create_supplier_duplicate_name(client):
    client.post(
        "/api/v1/suppliers/",
        json={
            "name": "Fornecedor ABC",
            "contact_email": "contato@abc.com"
        }
    )
    response = client.post(
        "/api/v1/suppliers/",
        json={
            "name": "Fornecedor ABC",
            "contact_email": "outro@abc.com"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_supplier(client):
    create_response = client.post(
        "/api/v1/suppliers/",
        json={
            "name": "Fornecedor ABC",
            "contact_email": "contato@abc.com"
        }
    )
    supplier_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/suppliers/{supplier_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == supplier_id
    assert data["name"] == "Fornecedor ABC"


def test_get_supplier_not_found(client):
    response = client.get("/api/v1/suppliers/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_suppliers(client):
    client.post(
        "/api/v1/suppliers/",
        json={"name": "Fornecedor A", "contact_email": "a@test.com"}
    )
    client.post(
        "/api/v1/suppliers/",
        json={"name": "Fornecedor B", "contact_email": "b@test.com"}
    )
    
    response = client.get("/api/v1/suppliers/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_update_supplier(client):
    create_response = client.post(
        "/api/v1/suppliers/",
        json={
            "name": "Fornecedor ABC",
            "contact_email": "contato@abc.com"
        }
    )
    supplier_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/v1/suppliers/{supplier_id}",
        json={"name": "Fornecedor XYZ", "contact_email": "contato@xyz.com"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Fornecedor XYZ"


def test_delete_supplier(client):
    create_response = client.post(
        "/api/v1/suppliers/",
        json={
            "name": "Fornecedor ABC",
            "contact_email": "contato@abc.com"
        }
    )
    supplier_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/suppliers/{supplier_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/api/v1/suppliers/{supplier_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

