# Gestão de Estoque

Sistema completo de gestão de estoque com backend em FastAPI e frontend em React.

## 🏗️ Arquitetura

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React + TypeScript + Vite
- **Clean Architecture**: Separação clara de responsabilidades

## 🚀 Início Rápido com Docker

### Subir tudo de uma vez:

```bash
docker-compose up --build
```

Isso vai subir:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432

### Parar os serviços:

```bash
docker-compose down
```

### Parar e remover volumes:

```bash
docker-compose down -v
```

## 📁 Estrutura do Projeto

```
gestao-estoque/
├── backend/          # API FastAPI
│   ├── app/
│   │   ├── api/      # Endpoints
│   │   ├── core/     # Configurações
│   │   ├── db/       # Database
│   │   ├── models/   # SQLAlchemy Models
│   │   ├── schemas/  # Pydantic Schemas
│   │   └── services/ # Lógica de negócio
│   └── Dockerfile
├── frontend/         # React App
│   ├── src/
│   │   ├── domain/   # Entidades
│   │   ├── infra/    # Serviços API
│   │   └── presentation/ # Componentes
│   └── Dockerfile
└── docker-compose.yml
```

## 🔧 Desenvolvimento Local

### Backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📝 Variáveis de Ambiente

### Backend (`backend/.env`)
```env
SQLALCHEMY_DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/gestao_estoque
```

### Frontend (`frontend/.env`) - Opcional
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🧪 Testes

### Backend
```bash
cd backend
poetry run pytest
```

## 📚 Documentação da API

Quando o backend estiver rodando:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
