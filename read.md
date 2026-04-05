# Finance Data Processing and Access Control Backend

## 📌 Project Overview

This project is a backend system for managing financial records with role-based access control. It allows different users (Viewer, Analyst, Admin) to interact with financial data based on their permissions.

The system supports CRUD operations, filtering, and dashboard-level analytics.

---

## ⚙️ Tech Stack

* Backend: FastAPI (Python)
* Database: SQLite
* ORM: SQLAlchemy
* Validation: Pydantic

---

## 🚀 How to Run

1. Install dependencies:

```
pip install fastapi uvicorn sqlalchemy pydantic
```

2. Run server:

```
uvicorn main:app --reload
```

3. Open browser:

* API: http://127.0.0.1:8000
* Docs: http://127.0.0.1:8000/docs

---

## 👤 Roles & Permissions

| Role    | Permissions                          |
| ------- | ------------------------------------ |
| Viewer  | View records only                    |
| Analyst | View + Dashboard                     |
| Admin   | Full access (Create, Update, Delete) |

---

## 📊 API Endpoints

### Users

* POST /users → Create user
* GET /users → List users

### Records

* POST /records → Create record (Admin only)
* GET /records → View records (All roles)
* PUT /records/{id} → Update (Admin only)
* DELETE /records/{id} → Delete (Admin only)

### Dashboard

* GET /dashboard/summary → Analytics (Analyst & Admin)

---

## 🔐 Access Control

Role-based access control is implemented using a custom `check_role` function that restricts API access based on user roles.

---

## 🔍 Features

* User and role management
* Financial record CRUD operations
* Filtering (type, category)
* Dashboard summary (income, expenses, balance)
* Role-based access control
* Input validation and error handling

---

## 📌 Assumptions

* Authentication is simplified using user_id
* SQLite is used for simplicity
* Roles are predefined (viewer, analyst, admin)

---

## 💡 Future Improvements

* JWT Authentication
* Pagination
* Advanced analytics
* Deployment

---
