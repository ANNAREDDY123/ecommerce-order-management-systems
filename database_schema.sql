CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE products(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    description TEXT,
    price FLOAT,
    stock INTEGER,
    category VARCHAR(100),
    is_active BOOLEAN
);

CREATE TABLE cart(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
);

CREATE TABLE orders(
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    total_amount FLOAT,
    order_status VARCHAR(50)
);

CREATE TABLE payments(
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    amount FLOAT,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50)
);
