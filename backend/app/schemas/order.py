from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class OrderBase(BaseModel):
    total_value: float = Field(..., ge=0, description="O valor total do pedido não pode ser negativo")

class OrderCreate(BaseModel):
    total_value: float = Field(default=0.0, ge=0, description="O valor total do pedido não pode ser negativo")

class OrderUpdate(BaseModel):
    total_value: Optional[float] = Field(None, gt=0, description="O valor total do pedido deve ser maior que zero")
    status: Optional[str] = Field(None, max_length=20, description="Status do pedido")

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantidade deve ser maior que zero")
    price: float = Field(..., gt=0, description="Preço deve ser maior que zero")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int

    model_config = ConfigDict(from_attributes=True)

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    status: str
    items: Optional[List[OrderItemResponse]] = None

    model_config = ConfigDict(from_attributes=True)