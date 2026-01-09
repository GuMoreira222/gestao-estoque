import { apiClient } from '../http/api.client';
import { Category, CategoryCreate, CategoryUpdate } from '@domain/entities/Category';

export class CategoryService {
  private readonly basePath = '/categories';

  async getAll(skip = 0, limit = 100): Promise<Category[]> {
    return apiClient.get<Category[]>(this.basePath, { params: { skip, limit } });
  }

  async getById(id: number): Promise<Category> {
    return apiClient.get<Category>(`${this.basePath}/${id}`);
  }

  async create(data: CategoryCreate): Promise<Category> {
    return apiClient.post<Category>(this.basePath, data);
  }

  async update(id: number, data: CategoryUpdate): Promise<Category> {
    return apiClient.put<Category>(`${this.basePath}/${id}`, data);
  }

  async delete(id: number): Promise<void> {
    return apiClient.delete<void>(`${this.basePath}/${id}`);
  }
}

export const categoryService = new CategoryService();

