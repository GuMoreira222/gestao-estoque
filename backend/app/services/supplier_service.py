from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.models.supplier import Supplier
from fastapi import HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class SupplierService:
    @staticmethod
    def create_supplier(db: Session, supplier: SupplierCreate) -> SupplierResponse:
        existing = db.scalar(select(Supplier).where(Supplier.name == supplier.name))
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um fornecedor com este nome"
            )
        
        try:
            db_supplier = Supplier(
                name=supplier.name,
                contact_email=supplier.contact_email,
                cnpj=supplier.cnpj
            )
            db.add(db_supplier)
            db.commit()
            db.refresh(db_supplier)
            return SupplierResponse.model_validate(db_supplier)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar fornecedor. Verifique se o nome já existe."
            )

    @staticmethod
    def get_supplier(db: Session, supplier_id: int) -> SupplierResponse:
        db_supplier = db.scalar(select(Supplier).where(Supplier.id == supplier_id))
        if not db_supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fornecedor com ID {supplier_id} não encontrado"
            )
        return SupplierResponse.model_validate(db_supplier)

    @staticmethod
    def update_supplier(db: Session, supplier_id: int, supplier: SupplierUpdate) -> SupplierResponse:
        db_supplier = db.scalar(select(Supplier).where(Supplier.id == supplier_id))
        if not db_supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fornecedor com ID {supplier_id} não encontrado"
            )
        
        update_data = supplier.model_dump(exclude_unset=True)
        if "name" in update_data:
            existing = db.scalar(
                select(Supplier).where(
                    Supplier.name == update_data["name"],
                    Supplier.id != supplier_id
                )
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Já existe um fornecedor com este nome"
                )
        
        try:
            for field, value in update_data.items():
                setattr(db_supplier, field, value)
            db.commit()
            db.refresh(db_supplier)
            return SupplierResponse.model_validate(db_supplier)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar fornecedor. Verifique se o nome já existe."
            )

    @staticmethod
    def delete_supplier(db: Session, supplier_id: int) -> None:
        db_supplier = db.scalar(select(Supplier).where(Supplier.id == supplier_id))
        if not db_supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fornecedor com ID {supplier_id} não encontrado"
            )
        
        if db_supplier.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível deletar fornecedor com produtos associados. "
                       "Remova ou mova os produtos antes de deletar o fornecedor."
            )
        
        try:
            db.delete(db_supplier)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao deletar fornecedor"
            )

    @staticmethod
    def get_all_suppliers(db: Session) -> List[SupplierResponse]:
        db_suppliers = db.scalars(select(Supplier)).all()
        return [SupplierResponse.model_validate(supplier) for supplier in db_suppliers]

