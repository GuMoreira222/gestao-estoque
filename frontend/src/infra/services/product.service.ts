import { apiClient } from '../http/api.client';
import { Product, ProductCreate, ProductUpdate } from '@domain/entities/Product';

export class ProductService {
  private readonly basePath = '/products';

  async getAll(skip = 0, limit = 100, includeRelations = false): Promise<Product[]> {
    return apiClient.get<Product[]>(this.basePath, {
      params: { skip, limit, include_relations: includeRelations },
    });
  }

  async getById(id: number, includeRelations = false): Promise<Product> {
    return apiClient.get<Product>(`${this.basePath}/${id}`, {
      params: { include_relations: includeRelations },
    });
  }

  async create(data: ProductCreate): Promise<Product> {
    return apiClient.post<Product>(this.basePath, data);
  }

  async update(id: number, data: ProductUpdate): Promise<Product> {
    return apiClient.put<Product>(`${this.basePath}/${id}`, data);
  }

  async delete(id: number): Promise<void> {
    return apiClient.delete<void>(`${this.basePath}/${id}`);
  }
}

export const productService = new ProductService();

