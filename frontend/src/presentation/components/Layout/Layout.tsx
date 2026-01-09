import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Layout.css';

interface LayoutProps {
  children: ReactNode;
}

export const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="navbar-brand">
          <h1>Gestão de Estoque</h1>
        </div>
        <div className="navbar-menu">
          <Link
            to="/categories"
            className={`nav-link ${isActive('/categories') ? 'active' : ''}`}
          >
            Categorias
          </Link>
          <Link
            to="/suppliers"
            className={`nav-link ${isActive('/suppliers') ? 'active' : ''}`}
          >
            Fornecedores
          </Link>
          <Link
            to="/products"
            className={`nav-link ${isActive('/products') ? 'active' : ''}`}
          >
            Produtos
          </Link>
          <Link
            to="/orders"
            className={`nav-link ${isActive('/orders') ? 'active' : ''}`}
          >
            Pedidos
          </Link>
        </div>
      </nav>
      <main className="main-content">{children}</main>
    </div>
  );
};

