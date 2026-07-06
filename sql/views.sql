DROP VIEW IF EXISTS vw_delivery_performance;
DROP VIEW IF EXISTS vw_review_summary;
DROP VIEW IF EXISTS vw_payment_summary;
DROP VIEW IF EXISTS vw_seller_performance;
DROP VIEW IF EXISTS vw_product_category_sales;
DROP VIEW IF EXISTS vw_monthly_revenue;
DROP VIEW IF EXISTS vw_order_sales_summary;

CREATE VIEW vw_order_sales_summary AS
SELECT
    o.order_id,
    o.order_status,
    o.order_purchase_timestamp,
    c.customer_city,
    c.customer_state,
    p.product_category_name_english,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS item_total
FROM fact_orders o
JOIN dim_customers c
    ON o.customer_id = c.customer_id
JOIN fact_order_items oi
    ON o.order_id = oi.order_id
JOIN dim_products p
    ON oi.product_id = p.product_id;

CREATE VIEW vw_monthly_revenue AS
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    SUM(price) AS product_revenue,
    SUM(freight_value) AS freight_revenue,
    SUM(item_total) AS total_revenue
FROM vw_order_sales_summary
WHERE order_status = 'delivered'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp);

CREATE VIEW vw_product_category_sales AS
SELECT
    product_category_name_english,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(price) AS product_revenue,
    SUM(freight_value) AS freight_revenue,
    SUM(item_total) AS total_revenue
FROM vw_order_sales_summary
WHERE order_status = 'delivered'
GROUP BY product_category_name_english;

CREATE VIEW vw_seller_performance AS
SELECT
    seller_id,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(price) AS product_revenue,
    SUM(freight_value) AS freight_revenue,
    SUM(item_total) AS total_revenue
FROM vw_order_sales_summary
WHERE order_status = 'delivered'
GROUP BY seller_id;

CREATE VIEW vw_payment_summary AS
SELECT
    payment_type,
    COUNT(*) AS payment_count,
    SUM(payment_value) AS total_payment_value,
    AVG(payment_value) AS average_payment_value
FROM fact_payments
GROUP BY payment_type;

CREATE VIEW vw_review_summary AS
SELECT
    review_score,
    COUNT(*) AS review_count
FROM fact_reviews
GROUP BY review_score;

CREATE VIEW vw_delivery_performance AS
SELECT
    order_id,
    order_status,
    order_purchase_timestamp,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    CASE
        WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 'On time'
        WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 'Late'
        ELSE 'Not delivered'
    END AS delivery_status
FROM fact_orders;