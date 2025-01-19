#!/usr/bin/env python
import os

import pandas as pd
import pyarrow.parquet as pq
import argparse
from sqlalchemy import create_engine
import requests

def ingest_data(params):
    user = params.user
    password = params.password
    db = params.db
    port = params.port
    hostname = params.hostname
    table_name = params.table_name
    url =  "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
    downloaded_parquet_file_name='yellow_tripdata_2024-01.parquet'

    # Define the batch size
    batch_size = 100000
    number_of_rows_inserted = 0
    max_rows_cap = 3 * batch_size

    # Download dataset file from website if file not present
    if not os.path.exists(downloaded_parquet_file_name) or os.path.getsize(downloaded_parquet_file_name) == 0:
        print("Parquet file doesn't exist, Downloading..")
        response = requests.get(url)
        with open(downloaded_parquet_file_name, 'wb') as f:
            f.write(response.content)
    else:
        print("Downloaded parquet file already exists, skipping new download..")

    parquet_file = pq.ParquetFile(downloaded_parquet_file_name)


    # Initialize an empty DataFrame to store the rows
    df = pd.DataFrame()

    # Create postgres engine
    engine = create_engine(f'postgresql://{user}:{password}@{hostname}:{port}/{db}')
    engine.connect()

    #Create table schema
    df.head(0).to_sql(name = "yellow_taxi_data", con=engine, if_exists='replace')
    pd.read_sql(f"select count(*) from {table_name};", con=engine)



    # Iterate over the file in batches
    for batch in parquet_file.iter_batches(batch_size=batch_size):

        # Limit max rows inserted to the table
        number_of_rows_inserted = number_of_rows_inserted + batch_size

        # Convert the batch to a pandas DataFrame
        df = batch.to_pandas()

        # Replace table if loading first batch
        load_mode = 'replace' if number_of_rows_inserted == batch_size else 'append'

        # Insert the DataFrame into the PostgreSQL table
        df.to_sql('yellow_taxi_data', engine, if_exists=load_mode, index=False)
        print(f' {number_of_rows_inserted} rows inserted into yellow_taxi_data table')

        if number_of_rows_inserted >= max_rows_cap:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ingest parquet file data to postgres")

    parser.add_argument("--user", type=str, help="postgres user name")
    parser.add_argument("--password",type=str, help="postgres password")
    parser.add_argument("--db", type=str, help="postgres db")
    parser.add_argument("--table_name", help="postgres table name")
    parser.add_argument("--port", help="postgres port", required=False, default=5432)
    parser.add_argument("--hostname", help="postgres hostname", required=False, default='localhost')
    parser.add_argument("--url", help="url of parquet dataset", required=False,
                        default="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet")

    args = parser.parse_args()
    ingest_data(args)
