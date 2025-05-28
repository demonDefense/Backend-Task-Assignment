# E-commerce Admin API (FastAPI)

This project is a back-end API for an e-commerce admin dashboard. It is developed in **Python** using **FastAPI** and connects to a **MySQL** database. The API provides endpoints for managing products, inventory, and analyzing sales data.

---

## ✅ Features (In Progress)

- [x] Database schema defined and created using SQLAlchemy.
- [x] MySQL connection using environment variables (`.env`).
- [ ] API endpoints for:
  - [ ] Sales status & revenue analytics
  - [ ] Inventory management
  - [x] Product CRUD
  - [x] Category CRUD
  - [ ] Users CRUD
- [ ] Dummy data script
  - [x] Products 
  - [x] Categories
  - [ ] Sales
  - [ ] Inventory
- [ ] Unit tests
  - [x] Products
  - [x] Categories
  - [ ] Sales
  - [ ] Inventory
- [ ] API documentation

---

## 📁 Project Structure

```bash
Backend-Task-Assignment/
├── app/
│   ├── api/endpoints/        # Route handlers
│   ├── crud/                 # Data access layer
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
├── database.py               # DB connection
├── main.py                   # FastAPI entry point
├── scripts/                  # Data seeding scripts
├── requirements.txt
└── README.md

