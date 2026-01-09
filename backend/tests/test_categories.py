import pytest
from fastapi import status


def test_create_category(client):
    response = client.post(
        "/api/v1/categories/",
        json={"name": "Eletrônicos", "description": "Produtos eletrônicos"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Eletrônicos"
    assert data["description"] == "Produtos eletrônicos"
    assert "id" in data


def test_create_category_duplicate_name(client):
    client.post(
        "/api/v1/categories/",
        json={"name": "Eletrônicos", "description": "Produtos eletrônicos"}
    )
    response = client.post(
        "/api/v1/categories/",
        json={"name": "Eletrônicos", "description": "Outra descrição"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_category(client):
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "Eletrônicos", "description": "Produtos eletrônicos"}
    )
    category_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "Eletrônicos"


def test_get_category_not_found(client):
    response = client.get("/api/v1/categories/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_categories(client):
    client.post(
        "/api/v1/categories/",
        json={"name": "Eletrônicos", "description": "Produtos eletrônicos"}
    )
    client.post(
        "/api/v1/categories/",
        json={"name": "Roupas", "description": "Roupas e acessórios"}
    )
    
    response = client.get("/api/v1/categories/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_update_category(client):
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "Eletrônicos", "description": "Produtos eletrônicos"}
    )
    category_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/v1/categories/{category_id}",
        json={"name": "Eletrônicos Atualizados", "description": "Nova descrição"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Eletrônicos Atualizados"
    assert data["description"] == "Nova descrição"


def test_update_category_not_found(client):
    response = client.put(
        "/api/v1/categories/999",
        json={"name": "Teste"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_category(client):
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "Eletrônicos", "description": "Produtos eletrônicos"}
    )
    category_id = create_response.json()["id"]
    
    response = client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = client.get(f"/api/v1/categories/{category_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_category_not_found(client):
    response = client.delete("/api/v1/categories/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

