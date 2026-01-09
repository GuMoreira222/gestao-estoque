from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier
from fastapi import HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError


class ProductService:
    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> ProductResponse:
        existing_sku = db.scalar(select(Product).where(Product.sku == product.sku))
        if existing_sku:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um produto com o SKU {product.sku}"
            )
        
        category = db.scalar(select(Category).where(Category.id == product.category_id))
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria com ID {product.category_id} não encontrada"
            )
        
        supplier = db.scalar(select(Supplier).where(Supplier.id == product.supplier_id))
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Fornecedor com ID {product.supplier_id} não encontrado"
            )
        
        try:
            db_product = Product(
                name=product.name,
                sku=product.sku,
                price=product.price,
                stock_quantity=product.stock_quantity,
                category_id=product.category_id,
                supplier_id=product.supplier_id
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return ProductResponse.model_validate(db_product)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao criar produto. Verifique se o SKU já existe."
            )

    @staticmethod
    def get_product(db: Session, product_id: int, include_relations: bool = False) -> ProductResponse:
        query = select(Product).where(Product.id == product_id)
        
        if include_relations:
            query = query.options(joinedload(Product.category), joinedload(Product.supplier))
        
        db_product = db.scalar(query)
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {product_id} não encontrado"
            )
        return ProductResponse.model_validate(db_product)

    @staticmethod
    def update_product(db: Session, product_id: int, product: ProductUpdate) -> ProductResponse:
        db_product = db.scalar(select(Product).where(Product.id == product_id))
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {product_id} não encontrado"
            )
        
        update_data = product.model_dump(exclude_unset=True)
        
        if "sku" in update_data:
            existing_sku = db.scalar(
                select(Product).where(
                    Product.sku == update_data["sku"],
                    Product.id != product_id
                )
            )
            if existing_sku:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Já existe um produto com o SKU {update_data['sku']}"
                )
        
        if "category_id" in update_data:
            category = db.scalar(select(Category).where(Category.id == update_data["category_id"]))
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Categoria com ID {update_data['category_id']} não encontrada"
                )
        
        if "supplier_id" in update_data:
            supplier = db.scalar(select(Supplier).where(Supplier.id == update_data["supplier_id"]))
            if not supplier:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Fornecedor com ID {update_data['supplier_id']} não encontrado"
                )
        
        try:
            for field, value in update_data.items():
                setattr(db_product, field, value)
            db.commit()
            db.refresh(db_product)
            return ProductResponse.model_validate(db_product)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao atualizar produto. Verifique se o SKU já existe."
            )

    @staticmethod
    def delete_product(db: Session, product_id: int) -> None:
        db_product = db.scalar(select(Product).where(Product.id == product_id))
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {product_id} não encontrado"
            )
        
        if db_product.order_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível deletar produto com itens de pedido associados. "
                       "Remova os itens dos pedidos antes de deletar o produto."
            )
        
        try:
            db.delete(db_product)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao deletar produto"
            )

    @staticmethod
    def get_all_products(db: Session, include_relations: bool = False) -> List[ProductResponse]:
        query = select(Product)
        
        if include_relations:
            query = query.options(joinedload(Product.category), joinedload(Product.supplier))
        
        db_products = db.scalars(query).unique().all()
        return [ProductResponse.model_validate(product) for product in db_products]

