-- CS4092 Project: Sample SQL Queries
-- Run against the database created by schema.sql

-- Query 1 (multi-table join): customers and the names of products they purchased
-- where the product price is greater than $100.
SELECT c.name AS customer_name, p.name AS product_name, p.price
FROM Customer c
JOIN Purchase pu ON pu.customer_id = c.customer_id
JOIN Product p ON p.product_id = pu.product_id
WHERE p.price > 100
ORDER BY c.name;

-- Query 2: total units sold and revenue per product, highest revenue first.
SELECT p.name AS product_name,
       SUM(pu.quantity) AS units_sold,
       ROUND(SUM(pu.quantity * p.price), 2) AS revenue
FROM Product p
JOIN Purchase pu ON pu.product_id = p.product_id
GROUP BY p.product_id
ORDER BY revenue DESC;

-- Query 3: each customer's total spend across all purchases, including customers
-- with zero purchases.
SELECT c.name AS customer_name,
       COALESCE(ROUND(SUM(pu.quantity * p.price), 2), 0) AS total_spend
FROM Customer c
LEFT JOIN Purchase pu ON pu.customer_id = c.customer_id
LEFT JOIN Product p ON p.product_id = pu.product_id
GROUP BY c.customer_id
ORDER BY total_spend DESC;

-- Query 4: products that are low on stock (fewer than 25 units remaining),
-- along with the staff member who added them.
SELECT p.name AS product_name, p.quantity_in_stock, s.name AS added_by
FROM Product p
JOIN Staff s ON s.staff_id = p.added_by_staff_id
WHERE p.quantity_in_stock < 25
ORDER BY p.quantity_in_stock ASC;
