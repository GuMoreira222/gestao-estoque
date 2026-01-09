import { useState } from 'react';
import { useProducts, useCreateProduct, useUpdateProduct, useDeleteProduct } from '@presentation/hooks/useProducts';
import { useCategories } from '@presentation/hooks/useCategories';
import { useSuppliers } from '@presentation/hooks/useSuppliers';
import { Product, ProductCreate, ProductUpdate } from '@domain/entities/Product';
import './Products.css';

export const Products = () => {
  const { data: products, isLoading, error } = useProducts(true);
  const { data: categories } = useCategories();
  const { data: suppliers } = useSuppliers();
  const createMutation = useCreateProduct();
  const updateMutation = useUpdateProduct();
  const deleteMutation = useDeleteProduct();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [formData, setFormData] = useState<ProductCreate>({
    name: '',
    sku: '',
    price: 0,
    stock_quantity: 0,
    category_id: 0,
    supplier_id: 0,
  });

  const handleOpenModal = (product?: Product) => {
    if (product) {
      setEditingProduct(product);
      setFormData({
        name: product.name,
        sku: product.sku,
        price: product.price,
        stock_quantity: product.stock_quantity,
        category_id: product.category_id,
        supplier_id: product.supplier_id,
      });
    } else {
      setEditingProduct(null);
      setFormData({
        name: '',
        sku: '',
        price: 0,
        stock_quantity: 0,
        category_id: categories?.[0]?.id || 0,
        supplier_id: suppliers?.[0]?.id || 0,
      });
    }
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingProduct(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingProduct) {
        await updateMutation.mutateAsync({ id: editingProduct.id, data: formData as ProductUpdate });
      } else {
        await createMutation.mutateAsync(formData);
      }
      handleCloseModal();
    } catch (error) {
      alert('Erro ao salvar produto');
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja deletar este produto?')) {
      try {
        await deleteMutation.mutateAsync(id);
      } catch (error) {
        alert('Erro ao deletar produto');
      }
    }
  };

  if (isLoading) return <div className="loading">Carregando...</div>;
  if (error) return <div className="error">Erro ao carregar produtos</div>;

  return (
    <div className="products-page">
      <div className="page-header">
        <h2>Produtos</h2>
        <button className="btn-primary" onClick={() => handleOpenModal()}>
          Novo Produto
        </button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>SKU</th>
              <th>Preço</th>
              <th>Estoque</th>
              <th>Categoria</th>
              <th>Fornecedor</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {products?.map((product) => (
              <tr key={product.id}>
                <td>{product.id}</td>
                <td>{product.name}</td>
                <td>{product.sku}</td>
                <td>R$ {product.price.toFixed(2)}</td>
                <td>{product.stock_quantity}</td>
                <td>{product.category?.name || '-'}</td>
                <td>{product.supplier?.name || '-'}</td>
                <td>
                  <button className="btn-edit" onClick={() => handleOpenModal(product)}>
                    Editar
                  </button>
                  <button className="btn-delete" onClick={() => handleDelete(product.id)}>
                    Deletar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {isModalOpen && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>{editingProduct ? 'Editar' : 'Novo'} Produto</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Nome *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  minLength={2}
                  maxLength={100}
                />
              </div>
              <div className="form-group">
                <label>SKU *</label>
                <input
                  type="text"
                  value={formData.sku}
                  onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                  required
                  maxLength={50}
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Preço *</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={formData.price}
                    onChange={(e) => setFormData({ ...formData, price: parseFloat(e.target.value) || 0 })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Estoque *</label>
                  <input
                    type="number"
                    min="0"
                    value={formData.stock_quantity}
                    onChange={(e) => setFormData({ ...formData, stock_quantity: parseInt(e.target.value) || 0 })}
                    required
                  />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Categoria *</label>
                  <select
                    value={formData.category_id}
                    onChange={(e) => setFormData({ ...formData, category_id: parseInt(e.target.value) })}
                    required
                  >
                    <option value={0}>Selecione...</option>
                    {categories?.map((cat) => (
                      <option key={cat.id} value={cat.id}>
                        {cat.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Fornecedor *</label>
                  <select
                    value={formData.supplier_id}
                    onChange={(e) => setFormData({ ...formData, supplier_id: parseInt(e.target.value) })}
                    required
                  >
                    <option value={0}>Selecione...</option>
                    {suppliers?.map((sup) => (
                      <option key={sup.id} value={sup.id}>
                        {sup.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="form-actions">
                <button type="button" className="btn-secondary" onClick={handleCloseModal}>
                  Cancelar
                </button>
                <button type="submit" className="btn-primary" disabled={createMutation.isLoading || updateMutation.isLoading}>
                  Salvar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

