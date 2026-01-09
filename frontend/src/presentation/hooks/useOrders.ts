import { useQuery, useMutation, useQueryClient } from 'react-query';
import { orderService } from '@infra/services/order.service';
import { Order, OrderCreate, OrderUpdate, OrderItem, OrderItemCreate } from '@domain/entities/Order';

export const useOrders = (includeItems = false) => {
  return useQuery<Order[], Error>(
    ['orders', includeItems],
    () => orderService.getAll(0, 100, includeItems)
  );
};

export const useOrder = (id: number, includeItems = true) => {
  return useQuery<Order, Error>(
    ['order', id, includeItems],
    () => orderService.getById(id, includeItems),
    {
      enabled: !!id,
    }
  );
};

export const useCreateOrder = () => {
  const queryClient = useQueryClient();
  return useMutation<Order, Error, OrderCreate>(
    (data) => orderService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('orders');
      },
    }
  );
};

export const useUpdateOrder = () => {
  const queryClient = useQueryClient();
  return useMutation<Order, Error, { id: number; data: OrderUpdate }>(
    ({ id, data }) => orderService.update(id, data),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries('orders');
        queryClient.invalidateQueries(['order', variables.id]);
      },
    }
  );
};

export const useDeleteOrder = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, number>(
    (id) => orderService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('orders');
      },
    }
  );
};

export const useAddOrderItem = () => {
  const queryClient = useQueryClient();
  return useMutation<OrderItem, Error, { orderId: number; item: OrderItemCreate }>(
    ({ orderId, item }) => orderService.addItem(orderId, item),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries(['order', variables.orderId]);
        queryClient.invalidateQueries('orders');
      },
    }
  );
};

export const useRemoveOrderItem = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, { orderId: number; itemId: number }>(
    ({ orderId, itemId }) => orderService.removeItem(orderId, itemId),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries(['order', variables.orderId]);
        queryClient.invalidateQueries('orders');
      },
    }
  );
};

export const useCompleteOrder = () => {
  const queryClient = useQueryClient();
  return useMutation<Order, Error, number>(
    (id) => orderService.complete(id),
    {
      onSuccess: (_, id) => {
        queryClient.invalidateQueries(['order', id]);
        queryClient.invalidateQueries('orders');
        queryClient.invalidateQueries('products');
      },
    }
  );
};

