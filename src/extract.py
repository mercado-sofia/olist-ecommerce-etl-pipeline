import pandas as pd
from pathlib import Path


FILES = {
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


def extract_olist_data(raw_dir: str = "data/raw") -> dict:
    """
    Read all raw Olist CSV files into Pandas DataFrames.
    """

    raw_path = Path(raw_dir)

    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data folder not found: {raw_path}")

    data = {}

    for name, filename in FILES.items():
        file_path = raw_path / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

        data[name] = pd.read_csv(file_path)

    return data


if __name__ == "__main__":
    data = extract_olist_data()

    for name, df in data.items():
        print(name, df.shape)