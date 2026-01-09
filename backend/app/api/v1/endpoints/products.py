from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return ProductService.create_product(db, product)


@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0,
    limit: int = 100,
    include_relations: bool = False,
    db: Session = Depends(get_db)
):
    products = ProductService.get_all_products(db, include_relations=include_relations)
    return products[skip:skip + limit] if limit else products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    include_relations: bool = False,
    db: Session = Depends(get_db)
):
    return ProductService.get_product(db, product_id, include_relations=include_relations)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    return ProductService.update_product(db, product_id, product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    ProductService.delete_product(db, product_id)
    return None

