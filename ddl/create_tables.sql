DROP TABLE IF EXISTS fact_orders CASCADE;
DROP TABLE IF EXISTS dim_customers CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_payments CASCADE;

-- Измерение: Клиенты
CREATE TABLE dim_customers (
    customer_id INTEGER PRIMARY KEY,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    city TEXT,
    created_at DATE
);

-- Измерение: Товары
CREATE TABLE dim_products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price DECIMAL(10,2),
    currency TEXT,
    is_active BOOLEAN
);

-- Измерение: Дата
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name TEXT,
    day INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

-- Измерение: Платежи
CREATE TABLE dim_payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    amount DECIMAL(10,2),
    currency TEXT,
    payment_method TEXT,
    payment_date DATE
);

-- Факт: Заказы (связываем с клиентами, продуктами, датой)
CREATE TABLE fact_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES dim_customers(customer_id),
    product_id INTEGER REFERENCES dim_products(product_id),
    order_date DATE REFERENCES dim_date(date_id),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    currency TEXT,
    total_amount DECIMAL(10,2),
    status TEXT
);

-- Индексы для производительности
CREATE INDEX idx_fact_customer ON fact_orders(customer_id);
CREATE INDEX idx_fact_product ON fact_orders(product_id);
CREATE INDEX idx_fact_date ON fact_orders(order_date);