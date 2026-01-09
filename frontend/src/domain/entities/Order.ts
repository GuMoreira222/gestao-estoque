export interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  price: number;
}

export interface Order {
  id: number;
  total_value: number;
  created_at: string;
  status: string;
  items?: OrderItem[];
}

export interface OrderCreate {
  total_value?: number;
}

export interface OrderUpdate {
  total_value?: number;
  status?: string;
}

export interface OrderItemCreate {
  product_id: number;
  quantity: number;
  price: number;
}

