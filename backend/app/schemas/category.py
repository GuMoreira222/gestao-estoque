from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nome da categoria")
    description: Optional[str] = Field(None, max_length=255, description="Descrição opcional")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)

class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)