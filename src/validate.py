def validate_relationships(tables: dict) -> list:
    """
    Validate primary keys, foreign keys, and important data quality rules.
    """

    errors = []

    customers = tables["dim_customers"]
    sellers = tables["dim_sellers"]
    products = tables["dim_products"]
    orders = tables["fact_orders"]
    items = tables["fact_order_items"]
    payments = tables["fact_payments"]
    reviews = tables["fact_reviews"]

    # Primary key uniqueness checks
    if customers["customer_id"].duplicated().any():
        errors.append("Duplicate customer_id found in dim_customers.")

    if sellers["seller_id"].duplicated().any():
        errors.append("Duplicate seller_id found in dim_sellers.")

    if products["product_id"].duplicated().any():
        errors.append("Duplicate product_id found in dim_products.")

    if orders["order_id"].duplicated().any():
        errors.append("Duplicate order_id found in fact_orders.")

    if reviews["review_id"].duplicated().any():
        errors.append("Duplicate review_id found in fact_reviews.")

    # Foreign key checks
    if not orders["customer_id"].isin(customers["customer_id"]).all():
        errors.append("Orders with unmatched customer_id found.")

    if not items["order_id"].isin(orders["order_id"]).all():
        errors.append("Order items with unmatched order_id found.")

    if not items["product_id"].isin(products["product_id"]).all():
        errors.append("Order items with unmatched product_id found.")

    if not items["seller_id"].isin(sellers["seller_id"]).all():
        errors.append("Order items with unmatched seller_id found.")

    if not payments["order_id"].isin(orders["order_id"]).all():
        errors.append("Payments with unmatched order_id found.")

    if not reviews["order_id"].isin(orders["order_id"]).all():
        errors.append("Reviews with unmatched order_id found.")

    # Value checks
    if (items["price"] < 0).any():
        errors.append("Negative item price found.")

    if (items["freight_value"] < 0).any():
        errors.append("Negative freight value found.")

    if (payments["payment_value"] < 0).any():
        errors.append("Negative payment value found.")

    if not reviews["review_score"].between(1, 5).all():
        errors.append("Review score outside 1 to 5 found.")

    # Date consistency check for delivered orders
    delivered_orders = orders[
        orders["order_status"] == "delivered"
    ].copy()

    invalid_delivery_dates = delivered_orders[
        delivered_orders["order_delivered_customer_date"]
        < delivered_orders["order_purchase_timestamp"]
    ]

    if not invalid_delivery_dates.empty:
        errors.append("Delivered date earlier than purchase date found.")

    return errors