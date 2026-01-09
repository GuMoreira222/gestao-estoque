import { useQuery, useMutation, useQueryClient } from 'react-query';
import { supplierService } from '@infra/services/supplier.service';
import { Supplier, SupplierCreate, SupplierUpdate } from '@domain/entities/Supplier';

export const useSuppliers = () => {
  return useQuery<Supplier[], Error>('suppliers', () => supplierService.getAll());
};

export const useSupplier = (id: number) => {
  return useQuery<Supplier, Error>(['supplier', id], () => supplierService.getById(id), {
    enabled: !!id,
  });
};

export const useCreateSupplier = () => {
  const queryClient = useQueryClient();
  return useMutation<Supplier, Error, SupplierCreate>(
    (data) => supplierService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('suppliers');
      },
    }
  );
};

export const useUpdateSupplier = () => {
  const queryClient = useQueryClient();
  return useMutation<Supplier, Error, { id: number; data: SupplierUpdate }>(
    ({ id, data }) => supplierService.update(id, data),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries('suppliers');
        queryClient.invalidateQueries(['supplier', variables.id]);
      },
    }
  );
};

export const useDeleteSupplier = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, number>(
    (id) => supplierService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('suppliers');
      },
    }
  );
};

