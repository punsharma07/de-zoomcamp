#!/usr/bin/env python

import os

from time import time
import pandas as pd
from sqlalchemy import create_engine

MY_CREDS_DICT = {
    "user" : "postgres",
    "password" : "postgres",
    "host" : "localhost",
    "port" : 5432,
    "db" : "ny_taxi",
}

TABLE = {
    "green_tripdata" : "green_tripdata",
    "taxi_zone_lookup" : "taxi_zone_lookup"
}

SOURCE_FILES = {
    "GREEN_TRIPDATA_FILE" : "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz",
    "TAXI_ZONE_LOOKUP_FILE" : "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
}


def download_file(source_file_url, table_name):
    if source_file_url.endswith('.csv.gz'):
        csv_name = table_name + '.csv.gz'
    else:
        csv_name = table_name + '.csv'
    os.system(f"wget {source_file_url} -O {csv_name}")
    return csv_name


def load_file_to_postgres_table(csv_name, table_name):
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=10000)
    df = next(df_iter)

    user = MY_CREDS_DICT.get("user")
    password = MY_CREDS_DICT.get("password")
    host = MY_CREDS_DICT.get("host")
    port = MY_CREDS_DICT.get("port")
    db = MY_CREDS_DICT.get("db")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    if table_name == 'green_tripdata':
        # cast datetime column to date time
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:

        try:
            t_start = time()
            df = next(df_iter)

            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break


if __name__ == '__main__':

    green_tripdata_csv = download_file(SOURCE_FILES.get("GREEN_TRIPDATA_FILE"), TABLE.get("green_tripdata"))
    taxi_zone_lookup_table_csv = download_file(SOURCE_FILES.get("TAXI_ZONE_LOOKUP_FILE"), TABLE.get("taxi_zone_lookup"))

    load_file_to_postgres_table(green_tripdata_csv, TABLE.get("green_tripdata"))
    load_file_to_postgres_table(taxi_zone_lookup_table_csv, TABLE.get("taxi_zone_lookup"))


