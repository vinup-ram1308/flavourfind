import pandas as pd
from google.cloud import bigquery
import os

PROJECT_ID = "flavourfind-491621"
DATASET_ID = "flavourfind"
TABLE_ID = "restaurants"
CSV_PATH = "cleaned_yelp_restaurants.csv"

def prepare_and_upload():
    print("Loading CSV...")
    df = pd.read_csv(CSV_PATH)

    print(f"Original shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    # Standardise column names to lowercase with underscores
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Keep only the columns we need
    required_cols = ["business_id", "name", "city", "state",
                     "stars", "review_count", "categories", "wifi_status"]
    df = df[[c for c in required_cols if c in df.columns]]

    # Drop rows missing critical fields
    df = df.dropna(subset=["name", "city", "categories"])

    # Clean up text fields
    df["name"] = df["name"].str.strip()
    df["city"] = df["city"].str.strip()
    df["state"] = df["state"].str.strip()
    df["categories"] = df["categories"].str.strip()

    # Normalise wifi_status — fill blanks as 'unknown'
    if "wifi_status" in df.columns:
        df["wifi_status"] = df["wifi_status"].fillna("unknown").str.lower().str.strip()

    # Ensure correct types
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce")
    df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce").astype("Int64")

    # Drop rows where stars is invalid
    df = df.dropna(subset=["stars"])

    print(f"Cleaned shape: {df.shape}")
    print(df.head(3))

    # Upload to BigQuery
    client = bigquery.Client(project=PROJECT_ID)

    # Create dataset if it doesn't exist
    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    dataset_ref.location = "US"
    try:
        client.create_dataset(dataset_ref, exists_ok=True)
        print(f"Dataset '{DATASET_ID}' ready.")
    except Exception as e:
        print(f"Dataset creation note: {e}")

    # Upload table
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
    )

    print(f"Uploading to BigQuery table: {table_ref} ...")
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    table = client.get_table(table_ref)
    print(f"Upload complete. {table.num_rows} rows in {table_ref}")

if __name__ == "__main__":
    prepare_and_upload()