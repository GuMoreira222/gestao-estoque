from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.models.category import Category
from fastapi import HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class CategoryService:
    @staticmethod
    def create_category(db: Session, category: CategoryCreate) -> CategoryResponse:
        existing = db.scalar(select(Category).where(Category.name == category.name))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe uma categoria com este nome"
            )
        
        try:
            db_category = Category(
                name=category.name,
                description=category.description
            )
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            return CategoryResponse.model_validate(db_category)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar categoria. Verifique se o nome já existe."
            )

    @staticmethod
    def get_category(db: Session, category_id: int) -> CategoryResponse:
        db_category = db.scalar(select(Category).where(Category.id == category_id))
        if not db_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria com ID {category_id} não encontrada"
            )
        return CategoryResponse.model_validate(db_category)

    @staticmethod
    def update_category(db: Session, category_id: int, category: CategoryUpdate) -> CategoryResponse:
        db_category = db.scalar(select(Category).where(Category.id == category_id))
        if not db_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria com ID {category_id} não encontrada"
            )
        
        update_data = category.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing = db.scalar(
                select(Category).where(
                    Category.name == update_data["name"],
                    Category.id != category_id
                )
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Já existe uma categoria com este nome"
                )
        
        try:
            for field, value in update_data.items():
                setattr(db_category, field, value)
            db.commit()
            db.refresh(db_category)
            return CategoryResponse.model_validate(db_category)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar categoria. Verifique se o nome já existe."
            )

    @staticmethod
    def delete_category(db: Session, category_id: int) -> None:
        db_category = db.scalar(select(Category).where(Category.id == category_id))
        if not db_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria com ID {category_id} não encontrada"
            )
        
        if db_category.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível deletar categoria com produtos associados. "
                       "Remova ou mova os produtos antes de deletar a categoria."
            )
        
        try:
            db.delete(db_category)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao deletar categoria"
            )

    @staticmethod
    def get_all_categories(db: Session) -> List[CategoryResponse]:
        db_categories = db.scalars(select(Category)).all()
        return [CategoryResponse.model_validate(category) for category in db_categories]