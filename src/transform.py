import pandas as pd
from pathlib import Path


def clean_olist_data(data: dict) -> dict:
    """
    Clean raw Olist data before modeling.
    """

    cleaned = {name: df.copy() for name, df in data.items()}

    # Convert order date columns
    orders = cleaned["orders"]

    order_date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for col in order_date_cols:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    # Convert order item date and numeric columns
    order_items = cleaned["order_items"]

    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"],
        errors="coerce"
    )

    order_items["price"] = pd.to_numeric(order_items["price"], errors="coerce")
    order_items["freight_value"] = pd.to_numeric(order_items["freight_value"], errors="coerce")

    # Convert payment numeric columns
    payments = cleaned["payments"]

    payments["payment_sequential"] = pd.to_numeric(
        payments["payment_sequential"],
        errors="coerce"
    )

    payments["payment_installments"] = pd.to_numeric(
        payments["payment_installments"],
        errors="coerce"
    )

    payments["payment_value"] = pd.to_numeric(
        payments["payment_value"],
        errors="coerce"
    )

    # Convert review dates
    reviews = cleaned["reviews"]

    reviews["review_creation_date"] = pd.to_datetime(
        reviews["review_creation_date"],
        errors="coerce"
    )

    reviews["review_answer_timestamp"] = pd.to_datetime(
        reviews["review_answer_timestamp"],
        errors="coerce"
    )

    # Convert product numeric columns
    products = cleaned["products"]

    product_numeric_cols = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for col in product_numeric_cols:
        products[col] = pd.to_numeric(products[col], errors="coerce")

    # Join product category English translation
    category_translation = cleaned["category_translation"]

    products = products.merge(
        category_translation,
        on="product_category_name",
        how="left"
    )

    cleaned["products"] = products

    return cleaned


def create_model_tables(cleaned: dict) -> dict:
    """
    Create dimension and fact tables from cleaned Olist data.
    """

    dim_customers = cleaned["customers"][
        [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ]
    ].drop_duplicates(subset=["customer_id"])

    dim_sellers = cleaned["sellers"][
        [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state",
        ]
    ].drop_duplicates(subset=["seller_id"])

    dim_products = cleaned["products"][
        [
            "product_id",
            "product_category_name",
            "product_category_name_english",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ]
    ].drop_duplicates(subset=["product_id"])

    fact_orders = cleaned["orders"][
        [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    ].drop_duplicates(subset=["order_id"])

    fact_order_items = cleaned["order_items"][
        [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value",
        ]
    ].drop_duplicates(subset=["order_id", "order_item_id"])

    fact_payments = cleaned["payments"][
        [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value",
        ]
    ]

    fact_reviews = cleaned["reviews"][
        [
            "review_id",
            "order_id",
            "review_score",
            "review_creation_date",
            "review_answer_timestamp",
        ]
    ].drop_duplicates(subset=["review_id"])

    tables = {
        "dim_customers": dim_customers,
        "dim_sellers": dim_sellers,
        "dim_products": dim_products,
        "fact_orders": fact_orders,
        "fact_order_items": fact_order_items,
        "fact_payments": fact_payments,
        "fact_reviews": fact_reviews,
    }

    return tables


def save_processed_tables(tables: dict, processed_dir: str = "data/processed") -> None:
    """
    Save modeled tables as CSV files in data/processed.
    """

    processed_path = Path(processed_dir)
    processed_path.mkdir(parents=True, exist_ok=True)

    for table_name, df in tables.items():
        output_path = processed_path / f"{table_name}.csv"
        df.to_csv(output_path, index=False)
        print(f"Saved {output_path}")