# E-commerce Admin API (FastAPI)

This project is a back-end API for an e-commerce admin dashboard. It is developed in **Python** using **FastAPI** and connects to a **MySQL** database. The API provides endpoints for managing users, roles, products, sales, and inventory, along with authentication and analytics features.

---

## ✅ Features

- [x] Database schema defined and created using SQLAlchemy ORM
- [x] Environment-based MySQL configuration using `.env`
- [x] Secure password hashing and JWT-based user authentication
- [x] Role-based access control
- [x] API Endpoints:
  - User & Role CRUD + Role Assignment
  - Product CRUD
  - Category CRUD
  - Sales CRUD, analytics by date, category, and revenue comparison
  - Inventory CRUD, low-stock detection, and inventory history tracking
- [x] Dummy data generation scripts:
  - Users + Roles
  - Products + Categories
  - Sales
  - Inventory
- [x] Built-in Swagger API documentation at `/docs`

---

## 📁 Project Structure

```bash
Backend-Task-Assignment/
├── app/
│   ├── api/endpoints/        # Route handlers for Users, Products, Sales, Inventory, etc.
│   │   ├── sales.py
│   │   ├── products.py
│   │   ├── category.py
│   │   ├── inventory.py
│   │   └── users.py
│   ├── crud/                 # Business logic and DB access
│   │   ├── sale_crud.py
│   │   ├── product_crud.py
│   │   ├── category_crud.py
│   │   ├── inventory_crud.py
│   │   └── user_crud.py
│   ├── models/               # SQLAlchemy ORM models
│   ├── schemas/              # Pydantic schemas for request/response
├── database.py               # DB connection and session management
├── main.py                   # FastAPI application setup
├── scripts/                  # Dummy data population scripts
│   ├── populate_sales_data.py
│   ├── populate_products_data.py
│   ├── populate_inventory_data.py
│   └── populate_user_data.py
├── requirements.txt          # Project dependencies
├── .env                      # Environment configuration (DB credentials)
└── README.md
```

---

## 🚀 How to Run

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Create and configure your `.env` file**:

```ini
DATABASE_URL=mysql+mysqlconnector://username:password@localhost:3306/database
SECRET_KEY=your_jwt_secret
```

3. **Run dummy data scripts** (optional):

```bash
python3 scripts/populate_user_data.py
python3 scripts/populate_products_data.py
python3 scripts/populate_sales_data.py
python3 scripts/populate_inventory_data.py
```

4. **Start the server**:

```bash
uvicorn main:app
```

5. **Visit API documentation**:

[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📬 Contact

For issues or contributions, please open an issue or pull request on the repository.

