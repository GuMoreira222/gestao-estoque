from app.db.session import Base
from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Float, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    sku: Mapped[str] = mapped_column(String(50), unique=True)
    price: Mapped[float] = mapped_column(Float)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    
    category: Mapped["Category"] = relationship(back_populates="products")
    supplier: Mapped["Supplier"] = relationship(back_populates="products")
    
    order_items: Mapped[List["OrderItem"]] = relationship(back_populates="product")