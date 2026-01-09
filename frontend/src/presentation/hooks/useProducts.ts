import { useQuery, useMutation, useQueryClient } from 'react-query';
import { productService } from '@infra/services/product.service';
import { Product, ProductCreate, ProductUpdate } from '@domain/entities/Product';

export const useProducts = (includeRelations = false) => {
  return useQuery<Product[], Error>(
    ['products', includeRelations],
    () => productService.getAll(0, 100, includeRelations)
  );
};

export const useProduct = (id: number, includeRelations = false) => {
  return useQuery<Product, Error>(
    ['product', id, includeRelations],
    () => productService.getById(id, includeRelations),
    {
      enabled: !!id,
    }
  );
};

export const useCreateProduct = () => {
  const queryClient = useQueryClient();
  return useMutation<Product, Error, ProductCreate>(
    (data) => productService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('products');
      },
    }
  );
};

export const useUpdateProduct = () => {
  const queryClient = useQueryClient();
  return useMutation<Product, Error, { id: number; data: ProductUpdate }>(
    ({ id, data }) => productService.update(id, data),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries('products');
        queryClient.invalidateQueries(['product', variables.id]);
      },
    }
  );
};

export const useDeleteProduct = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, number>(
    (id) => productService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('products');
      },
    }
  );
};

