-- 1. Monthly revenue
SELECT
    month,
    product_revenue,
    freight_revenue,
    total_revenue
FROM vw_monthly_revenue
ORDER BY month;

-- 2. Top 10 product categories by revenue
SELECT
    product_category_name_english,
    total_orders,
    product_revenue,
    freight_revenue,
    total_revenue
FROM vw_product_category_sales
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. Payment method distribution
SELECT
    payment_type,
    payment_count,
    total_payment_value,
    average_payment_value
FROM vw_payment_summary
ORDER BY total_payment_value DESC;

-- 5. Top 10 sellers by revenue
SELECT
    seller_id,
    total_orders,
    product_revenue,
    freight_revenue,
    total_revenue
FROM vw_seller_performance
ORDER BY total_revenue DESC
LIMIT 10;

-- 6. Delivery performance count
SELECT
    delivery_status,
    COUNT(*) AS order_count
FROM vw_delivery_performance
GROUP BY delivery_status
ORDER BY order_count DESC;