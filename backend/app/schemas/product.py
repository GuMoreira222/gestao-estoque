from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.schemas.category import CategoryResponse
from app.schemas.supplier import SupplierResponse

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome do produto")
    sku: str = Field(..., min_length=1, max_length=50, description="Código único de estoque (ex: PROD-001)")
    price: float = Field(..., gt=0, description="O preço deve ser maior que zero")
    stock_quantity: int = Field(default=0, ge=0, description="Quantidade não pode ser negativa")

class ProductCreate(ProductBase):
    category_id: int = Field(..., description="ID da categoria")
    supplier_id: int = Field(..., description="ID do fornecedor")

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0, description="O preço deve ser maior que zero")
    stock_quantity: Optional[int] = Field(None, ge=0, description="Quantidade não pode ser negativa")
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    category_id: int
    supplier_id: int
    category: Optional[CategoryResponse] = None
    supplier: Optional[SupplierResponse] = None

    model_config = ConfigDict(from_attributes=True)