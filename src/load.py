import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def get_database_engine():
    """
    Create SQLAlchemy database engine using credentials from .env.
    """

    load_dotenv()

    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")

    if not all([db_name, db_user, db_password, db_host, db_port]):
        raise ValueError("Missing database credentials in .env file.")

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_password,
        host=db_host,
        port=int(db_port),
        database=db_name,
    )

    return create_engine(database_url)


def load_tables_to_postgres(tables: dict) -> None:
    """
    Load modeled tables into PostgreSQL.
    Make sure sql/schema.sql has already been run before this.
    """

    engine = get_database_engine()

    load_order = [
        "dim_customers",
        "dim_sellers",
        "dim_products",
        "fact_orders",
        "fact_order_items",
        "fact_payments",
        "fact_reviews",
    ]

    for table_name in load_order:
        tables[table_name].to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False
        )

        print(f"Loaded {table_name} into PostgreSQL.")