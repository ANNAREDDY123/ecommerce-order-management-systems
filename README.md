# ecommerce-order-management-systems
FastAPI E-Commerce Order Management System with JWT Authentication, Product Management, Shopping Cart, Order Processing, Payment Integration, SQLAlchemy ORM, Pagination, Docker, and Clean Architecture.
# E-Commerce Order Management System

## Features

- JWT Authentication
- Product Management
- Shopping Cart
- Order Management
- Payment Management
- Filtering & Pagination
- SQLAlchemy ORM
- SQLite Database
- Docker Support

## Setup Instructions

1. Install dependencies:
   pip install -r requirements.txt

2. Run the application:
   uvicorn main:app --reload

## Environment Variables

SECRET_KEY=ecommerce_secret_key

ALGORITHM=HS256

## Authentication Flow

- Register using `/auth/register`
- Login using `/auth/login`
- JWT token is returned after successful login.

## API Flow Overview

- Register/Login
- Create Products
- Add Products to Cart
- Place Order
- Make Payment

## Assumptions Made

- One payment per order.
- Soft delete for products.
- Stock is reduced after successful order creation.
- Duplicate product names are not allowed.
