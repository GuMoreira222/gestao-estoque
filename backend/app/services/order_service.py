from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderItemResponse
from app.models.order import Order, OrderItem
from app.models.product import Product
from fastapi import HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError


class OrderService:
    @staticmethod
    def create_order(db: Session, order: OrderCreate) -> OrderResponse:
        try:
            db_order = Order(
                total_value=order.total_value,
                status="pending"
            )
            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            return OrderResponse.model_validate(db_order)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar pedido"
            )

    @staticmethod
    def get_order(db: Session, order_id: int, include_items: bool = True) -> OrderResponse:
        query = select(Order).where(Order.id == order_id)
        
        if include_items:
            query = query.options(joinedload(Order.items))
        
        db_order = db.scalar(query)
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido com ID {order_id} não encontrado"
            )
        return OrderResponse.model_validate(db_order)

    @staticmethod
    def update_order(db: Session, order_id: int, order: OrderUpdate) -> OrderResponse:
        db_order = db.scalar(select(Order).where(Order.id == order_id))
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido com ID {order_id} não encontrado"
            )
        
        update_data = order.model_dump(exclude_unset=True)
        
        if "status" in update_data:
            valid_statuses = ["pending", "processing", "completed", "cancelled"]
            if update_data["status"] not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Status inválido. Status válidos: {', '.join(valid_statuses)}"
                )
        
        try:
            for field, value in update_data.items():
                setattr(db_order, field, value)
            db.commit()
            db.refresh(db_order)
            return OrderResponse.model_validate(db_order)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar pedido"
            )

    @staticmethod
    def delete_order(db: Session, order_id: int) -> None:
        db_order = db.scalar(select(Order).where(Order.id == order_id))
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido com ID {order_id} não encontrado"
            )
        
        try:
            db.delete(db_order)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao deletar pedido"
            )

    @staticmethod
    def get_all_orders(db: Session, include_items: bool = False) -> List[OrderResponse]:
        query = select(Order)
        
        if include_items:
            query = query.options(joinedload(Order.items))
        
        db_orders = db.scalars(query).unique().all()
        return [OrderResponse.model_validate(order) for order in db_orders]

    @staticmethod
    def add_item_to_order(
        db: Session, 
        order_id: int, 
        product_id: int, 
        quantity: int, 
        price: float
    ) -> OrderItemResponse:
        db_order = db.scalar(select(Order).where(Order.id == order_id))
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido com ID {order_id} não encontrado"
            )
        
        db_product = db.scalar(select(Product).where(Product.id == product_id))
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {product_id} não encontrado"
            )
        
        if db_order.status != "cancelled":
            if db_product.stock_quantity < quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estoque insuficiente. Disponível: {db_product.stock_quantity}, Solicitado: {quantity}"
                )
        
        try:
            db_item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                price=price
            )
            db.add(db_item)
            
            db_order.total_value += (price * quantity)
            
            db.commit()
            db.refresh(db_item)
            return OrderItemResponse.model_validate(db_item)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao adicionar item ao pedido"
            )

    @staticmethod
    def remove_item_from_order(db: Session, order_id: int, item_id: int) -> None:
        db_item = db.scalar(
            select(OrderItem).where(
                OrderItem.id == item_id,
                OrderItem.order_id == order_id
            )
        )
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item com ID {item_id} não encontrado no pedido {order_id}"
            )
        
        db_order = db_item.order
        db_product = db_item.product
        
        try:
            db_order.total_value -= (db_item.price * db_item.quantity)
            
            db.delete(db_item)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao remover item do pedido"
            )

    @staticmethod
    def complete_order(db: Session, order_id: int) -> OrderResponse:
        db_order = db.scalar(
            select(Order).options(joinedload(Order.items)).where(Order.id == order_id)
        )
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido com ID {order_id} não encontrado"
            )
        
        if db_order.status == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pedido já está completado"
            )
        
        if db_order.status == "cancelled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível completar um pedido cancelado"
            )
        
        for item in db_order.items:
            product = db.scalar(select(Product).where(Product.id == item.product_id))
            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estoque insuficiente para o produto {product.name}. "
                           f"Disponível: {product.stock_quantity}, Necessário: {item.quantity}"
                )
        
        try:
            for item in db_order.items:
                product = db.scalar(select(Product).where(Product.id == item.product_id))
                product.stock_quantity -= item.quantity
            
            db_order.status = "completed"
            db.commit()
            db.refresh(db_order)
            return OrderResponse.model_validate(db_order)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao completar pedido"
            )

