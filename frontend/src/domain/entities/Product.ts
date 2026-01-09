import { Category } from './Category';
import { Supplier } from './Supplier';

export interface Product {
  id: number;
  name: string;
  sku: string;
  price: number;
  stock_quantity: number;
  category_id: number;
  supplier_id: number;
  category?: Category;
  supplier?: Supplier;
}

export interface ProductCreate {
  name: string;
  sku: string;
  price: number;
  stock_quantity: number;
  category_id: number;
  supplier_id: number;
}

export interface ProductUpdate {
  name?: string;
  sku?: string;
  price?: number;
  stock_quantity?: number;
  category_id?: number;
  supplier_id?: number;
}

