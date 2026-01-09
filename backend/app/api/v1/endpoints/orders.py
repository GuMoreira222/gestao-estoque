from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db
from app.schemas.order import (
    OrderCreate, 
    OrderUpdate, 
    OrderResponse, 
    OrderItemResponse,
    OrderItemCreate
)
from app.services.order_service import OrderService

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return OrderService.create_order(db, order)


@router.get("/", response_model=List[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    include_items: bool = False,
    db: Session = Depends(get_db)
):
    orders = OrderService.get_all_orders(db, include_items=include_items)
    return orders[skip:skip + limit] if limit else orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    include_items: bool = True,
    db: Session = Depends(get_db)
):
    return OrderService.get_order(db, order_id, include_items=include_items)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db)
):
    return OrderService.update_order(db, order_id, order)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    OrderService.delete_order(db, order_id)
    return None


@router.post("/{order_id}/items", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
def add_item_to_order(
    order_id: int,
    item: OrderItemCreate,
    db: Session = Depends(get_db)
):
    return OrderService.add_item_to_order(
        db, 
        order_id, 
        item.product_id, 
        item.quantity, 
        item.price
    )


@router.delete("/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_order(
    order_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    OrderService.remove_item_from_order(db, order_id, item_id)
    return None


@router.post("/{order_id}/complete", response_model=OrderResponse)
def complete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return OrderService.complete_order(db, order_id)

