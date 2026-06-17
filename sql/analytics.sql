-- 1. Топ-10 клиентов по сумме покупок (в их валюте, но без приведения)
SELECT 
    c.full_name AS customer_name,
    SUM(f.total_amount) AS total_spent
FROM fact_orders f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY total_spent DESC
LIMIT 10;

-- 2. Выручка по месяцам (сумма по всем заказам)
SELECT 
    d.year,
    d.month,
    d.month_name,
    SUM(f.total_amount) AS revenue
FROM fact_orders f
JOIN dim_date d ON f.order_date = d.date_id
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- 3. Самые популярные товары (по количеству проданных единиц)
SELECT 
    p.product_name,
    p.category,
    SUM(f.quantity) AS total_sold,
    SUM(f.total_amount) AS revenue
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_sold DESC
LIMIT 10;

-- 4. Последняя активность (дата) топ-5 пользователей по сумме покупок
WITH top_customers AS (
    SELECT 
        customer_id,
        SUM(total_amount) AS total_spent
    FROM fact_orders
    GROUP BY customer_id
    ORDER BY total_spent DESC
    LIMIT 5
)
SELECT 
    c.full_name,
    tc.total_spent,
    MAX(f.order_date) AS last_activity_date
FROM top_customers tc
JOIN dim_customers c ON tc.customer_id = c.customer_id
JOIN fact_orders f ON c.customer_id = f.customer_id
GROUP BY c.customer_id, c.full_name, tc.total_spent
ORDER BY tc.total_spent DESC;

-- 5. Пользователи без заказов
SELECT 
    c.customer_id,
    c.full_name,
    c.email
FROM dim_customers c
LEFT JOIN fact_orders f ON c.customer_id = f.customer_id
WHERE f.order_id IS NULL;