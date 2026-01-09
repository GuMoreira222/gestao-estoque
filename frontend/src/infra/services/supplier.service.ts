import { apiClient } from '../http/api.client';
import { Supplier, SupplierCreate, SupplierUpdate } from '@domain/entities/Supplier';

export class SupplierService {
  private readonly basePath = '/suppliers';

  async getAll(skip = 0, limit = 100): Promise<Supplier[]> {
    return apiClient.get<Supplier[]>(this.basePath, { params: { skip, limit } });
  }

  async getById(id: number): Promise<Supplier> {
    return apiClient.get<Supplier>(`${this.basePath}/${id}`);
  }

  async create(data: SupplierCreate): Promise<Supplier> {
    return apiClient.post<Supplier>(this.basePath, data);
  }

  async update(id: number, data: SupplierUpdate): Promise<Supplier> {
    return apiClient.put<Supplier>(`${this.basePath}/${id}`, data);
  }

  async delete(id: number): Promise<void> {
    return apiClient.delete<void>(`${this.basePath}/${id}`);
  }
}

export const supplierService = new SupplierService();

