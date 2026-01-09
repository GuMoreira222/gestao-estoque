import { useState } from 'react';
import { useOrders, useCreateOrder, useDeleteOrder, useAddOrderItem, useRemoveOrderItem, useCompleteOrder } from '@presentation/hooks/useOrders';
import { useProducts } from '@presentation/hooks/useProducts';
import { Order, OrderItemCreate } from '@domain/entities/Order';
import './Orders.css';

export const Orders = () => {
  const { data: orders, isLoading, error } = useOrders(true);
  const { data: products } = useProducts();
  const createMutation = useCreateOrder();
  const deleteMutation = useDeleteOrder();
  const addItemMutation = useAddOrderItem();
  const removeItemMutation = useRemoveOrderItem();
  const completeMutation = useCompleteOrder();

  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [itemForm, setItemForm] = useState<OrderItemCreate>({ product_id: 0, quantity: 1, price: 0 });

  const handleCreateOrder = async () => {
    try {
      await createMutation.mutateAsync({ total_value: 0 });
    } catch (error) {
      alert('Erro ao criar pedido');
    }
  };

  const handleDeleteOrder = async (id: number) => {
    if (confirm('Tem certeza que deseja deletar este pedido?')) {
      try {
        await deleteMutation.mutateAsync(id);
      } catch (error) {
        alert('Erro ao deletar pedido');
      }
    }
  };

  const handleAddItem = async (orderId: number) => {
    if (!itemForm.product_id || itemForm.quantity <= 0 || itemForm.price <= 0) {
      alert('Preencha todos os campos do item');
      return;
    }
    try {
      await addItemMutation.mutateAsync({ orderId, item: itemForm });
      setItemForm({ product_id: 0, quantity: 1, price: 0 });
    } catch (error) {
      alert('Erro ao adicionar item');
    }
  };

  const handleRemoveItem = async (orderId: number, itemId: number) => {
    try {
      await removeItemMutation.mutateAsync({ orderId, itemId });
    } catch (error) {
      alert('Erro ao remover item');
    }
  };

  const handleCompleteOrder = async (id: number) => {
    if (confirm('Deseja completar este pedido? O estoque será atualizado.')) {
      try {
        await completeMutation.mutateAsync(id);
      } catch (error) {
        alert('Erro ao completar pedido');
      }
    }
  };

  const handleProductChange = (productId: number) => {
    const product = products?.find((p) => p.id === productId);
    setItemForm({
      product_id: productId,
      quantity: itemForm.quantity,
      price: product?.price || 0,
    });
  };

  if (isLoading) return <div className="loading">Carregando...</div>;
  if (error) return <div className="error">Erro ao carregar pedidos</div>;

  return (
    <div className="orders-page">
      <div className="page-header">
        <h2>Pedidos</h2>
        <button className="btn-primary" onClick={handleCreateOrder}>
          Novo Pedido
        </button>
      </div>

      <div className="orders-grid">
        {orders?.map((order) => (
          <div key={order.id} className="order-card">
            <div className="order-header">
              <div>
                <h3>Pedido #{order.id}</h3>
                <p className="order-date">
                  {new Date(order.created_at).toLocaleDateString('pt-BR')}
                </p>
              </div>
              <div className="order-status">
                <span className={`status-badge status-${order.status}`}>
                  {order.status}
                </span>
              </div>
            </div>
            <div className="order-total">
              <strong>Total: R$ {order.total_value.toFixed(2)}</strong>
            </div>
            {order.items && order.items.length > 0 && (
              <div className="order-items">
                <h4>Itens:</h4>
                <ul>
                  {order.items.map((item) => (
                    <li key={item.id}>
                      {item.quantity}x - R$ {item.price.toFixed(2)} = R${' '}
                      {(item.quantity * item.price).toFixed(2)}
                      {selectedOrder?.id === order.id && (
                        <button
                          className="btn-remove-item"
                          onClick={() => handleRemoveItem(order.id, item.id)}
                        >
                          ×
                        </button>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {selectedOrder?.id === order.id && (
              <div className="add-item-form">
                <h4>Adicionar Item</h4>
                <select
                  value={itemForm.product_id}
                  onChange={(e) => handleProductChange(parseInt(e.target.value))}
                >
                  <option value={0}>Selecione o produto...</option>
                  {products?.map((product) => (
                    <option key={product.id} value={product.id}>
                      {product.name} - R$ {product.price.toFixed(2)} (Estoque: {product.stock_quantity})
                    </option>
                  ))}
                </select>
                <input
                  type="number"
                  min="1"
                  value={itemForm.quantity}
                  onChange={(e) => setItemForm({ ...itemForm, quantity: parseInt(e.target.value) || 1 })}
                  placeholder="Quantidade"
                />
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  value={itemForm.price}
                  onChange={(e) => setItemForm({ ...itemForm, price: parseFloat(e.target.value) || 0 })}
                  placeholder="Preço"
                />
                <button
                  className="btn-primary"
                  onClick={() => handleAddItem(order.id)}
                >
                  Adicionar
                </button>
              </div>
            )}
            <div className="order-actions">
              <button
                className="btn-edit"
                onClick={() => setSelectedOrder(selectedOrder?.id === order.id ? null : order)}
              >
                {selectedOrder?.id === order.id ? 'Fechar' : 'Gerenciar'}
              </button>
              {order.status !== 'completed' && (
                <button
                  className="btn-complete"
                  onClick={() => handleCompleteOrder(order.id)}
                >
                  Completar
                </button>
              )}
              <button className="btn-delete" onClick={() => handleDeleteOrder(order.id)}>
                Deletar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

