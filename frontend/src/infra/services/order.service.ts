import { apiClient } from '../http/api.client';
import { Order, OrderCreate, OrderUpdate, OrderItem, OrderItemCreate } from '@domain/entities/Order';

export class OrderService {
  private readonly basePath = '/orders';

  async getAll(skip = 0, limit = 100, includeItems = false): Promise<Order[]> {
    return apiClient.get<Order[]>(this.basePath, {
      params: { skip, limit, include_items: includeItems },
    });
  }

  async getById(id: number, includeItems = true): Promise<Order> {
    return apiClient.get<Order>(`${this.basePath}/${id}`, {
      params: { include_items: includeItems },
    });
  }

  async create(data: OrderCreate): Promise<Order> {
    return apiClient.post<Order>(this.basePath, data);
  }

  async update(id: number, data: OrderUpdate): Promise<Order> {
    return apiClient.put<Order>(`${this.basePath}/${id}`, data);
  }

  async delete(id: number): Promise<void> {
    return apiClient.delete<void>(`${this.basePath}/${id}`);
  }

  async addItem(orderId: number, item: OrderItemCreate): Promise<OrderItem> {
    return apiClient.post<OrderItem>(`${this.basePath}/${orderId}/items`, item);
  }

  async removeItem(orderId: number, itemId: number): Promise<void> {
    return apiClient.delete<void>(`${this.basePath}/${orderId}/items/${itemId}`);
  }

  async complete(orderId: number): Promise<Order> {
    return apiClient.post<Order>(`${this.basePath}/${orderId}/complete`);
  }
}

export const orderService = new OrderService();

