export interface Supplier {
  id: number;
  name: string;
  contact_email: string;
  cnpj?: string;
}

export interface SupplierCreate {
  name: string;
  contact_email: string;
  cnpj?: string;
}

export interface SupplierUpdate {
  name?: string;
  contact_email?: string;
  cnpj?: string;
}

