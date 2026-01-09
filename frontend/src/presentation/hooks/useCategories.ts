import { useQuery, useMutation, useQueryClient } from 'react-query';
import { categoryService } from '@infra/services/category.service';
import { Category, CategoryCreate, CategoryUpdate } from '@domain/entities/Category';

export const useCategories = () => {
  return useQuery<Category[], Error>('categories', () => categoryService.getAll());
};

export const useCategory = (id: number) => {
  return useQuery<Category, Error>(['category', id], () => categoryService.getById(id), {
    enabled: !!id,
  });
};

export const useCreateCategory = () => {
  const queryClient = useQueryClient();
  return useMutation<Category, Error, CategoryCreate>(
    (data) => categoryService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('categories');
      },
    }
  );
};

export const useUpdateCategory = () => {
  const queryClient = useQueryClient();
  return useMutation<Category, Error, { id: number; data: CategoryUpdate }>(
    ({ id, data }) => categoryService.update(id, data),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries('categories');
        queryClient.invalidateQueries(['category', variables.id]);
      },
    }
  );
};

export const useDeleteCategory = () => {
  const queryClient = useQueryClient();
  return useMutation<void, Error, number>(
    (id) => categoryService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('categories');
      },
    }
  );
};

