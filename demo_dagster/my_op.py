from datetime import datetime
from pathlib import Path
from dagster import op, get_dagster_logger
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import os
import pyarrow



@op
def fetch(dataset_url):
    """Fetch the data from the URL"""
    df = pd.read_csv(dataset_url)
    return df


@op
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean taxi data"""
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    df = df[df['passenger_count'] != 0]
    return df


@op
def write_db(df: pd.DataFrame, db_conn_string: str, table_name: str):
    """Write DF to a database"""
    time = datetime.now().strftime("%d-%m-%YT%H_%M_%S")
    table_name_t = f"{table_name}_{time}"
    connection = create_engine(db_conn_string)
    df.head(n=0).to_sql(name=table_name, con=connection, if_exists='append')
    df.to_sql(name=table_name_t, con=connection,
              if_exists='append', chunksize=10000)


@op
def my_op(context):
    context.log.info("my operations is starting")

    pgdb = psycopg2.connect(
        host="postgres",
        user="test",
        password="example",
        database="test"
    )

    mycursor = pgdb.cursor()

    DATA_SOURCE_LOCATION = os.path.abspath(os.path.join(os.path.dirname(
        __file__), 'dataset.xlsx'))
    context.log.info(DATA_SOURCE_LOCATION)

    df = pd.read_excel(DATA_SOURCE_LOCATION, names=None, engine='openpyxl')
    df = df.where((pd.notnull(df)), None)

    df = df.where(df != "#REF!", None)
    df = df.where(df != "!", None)
    df = df.where(df != "-", None)
    df = df.where(df != " ", None)
    df = df.where(df != "?", None)

    cols = ", ".join([str(i).replace(' ', '_') for i in df.columns.tolist()])
    print(cols)
    i = 0
    for row in df.iterrows():
        sql = "INSERT INTO drillingparameter (" + cols + ") VALUES ({})".format(
            ','.join(['%s']*len(df.columns)))
        mycursor.execute(sql, tuple(row[1]))
        pgdb.commit()
        context.log.info(f"inserting data {i} : {tuple(row[1])}")
        i += 1
