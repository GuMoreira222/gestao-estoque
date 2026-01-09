from app.db.session import Base
from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    contact_email: Mapped[str] = mapped_column(String(100))
    cnpj: Mapped[Optional[str]] = mapped_column(String(18))
    
    products: Mapped[List["Product"]] = relationship(back_populates="supplier")