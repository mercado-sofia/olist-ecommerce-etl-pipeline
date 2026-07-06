from extract import extract_olist_data
from transform import clean_olist_data, create_model_tables, save_processed_tables
from validate import validate_relationships
from load import load_tables_to_postgres


def main():
    print("Starting Olist ETL pipeline...")

    print("Extracting raw CSV files...")
    raw_data = extract_olist_data("data/raw")

    print("Cleaning raw data...")
    cleaned_data = clean_olist_data(raw_data)

    print("Creating dimension and fact tables...")
    modeled_tables = create_model_tables(cleaned_data)

    print("Validating modeled tables...")
    validation_errors = validate_relationships(modeled_tables)

    if validation_errors:
        print("Validation failed:")
        for error in validation_errors:
            print("-", error)

        raise ValueError("ETL stopped because validation errors were found.")

    print("Validation passed.")

    print("Saving processed CSV files...")
    save_processed_tables(modeled_tables, "data/processed")

    # Uncomment this after you create the PostgreSQL database
    # and run sql/schema.sql.
    #
    # print("Loading data into PostgreSQL...")
    # load_tables_to_postgres(modeled_tables)

    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()