from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nome do fornecedor")
    contact_email: EmailStr = Field(..., description="Email de contato")
    cnpj: Optional[str] = Field(None, max_length=18, description="CNPJ do fornecedor")

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    contact_email: Optional[EmailStr] = Field(None, description="Email de contato")
    cnpj: Optional[str] = Field(None, max_length=18)

class SupplierResponse(SupplierBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
