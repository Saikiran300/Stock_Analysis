from airflow import DAG
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta, timezone
import yfinance as yf
import pandas as pd
import pendulum

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='lab2_etl_stock',
    schedule_interval='@daily',
    start_date=datetime(2024, 9, 25),
    catchup=False,
    default_args=default_args,
    description='Daily ETL for AAPL and GOOGL using yfinance and Snowflake',
) as dag:

    @task
    def fetch_stock_data():
        symbols = ['AAPL', 'GOOGL']
        end = pendulum.now('UTC')
        start = end.subtract(days=180)
        rows = []

        for sym in symbols:
            # download 180 days of price data
            df = yf.download(
                sym,
                start=start.to_date_string(),
                end=end.to_date_string(),
                group_by='column',
                progress=False,
                auto_adjust=False
            )
            if df.empty:
                raise ValueError(f"No data fetched for {sym}")

            # select & rename
            df = (
                df
                .reset_index()[['Date','Open','High','Low','Close','Volume']]
                .rename(columns={
                    'Date':   'date',
                    'Open':   'open',
                    'High':   'high',
                    'Low':    'low',
                    'Close':  'close',
                    'Volume': 'volume'
                })
            )

            # flatten any MultiIndex (if present)
            if getattr(df.columns, 'nlevels', 1) > 1:
                df.columns = df.columns.get_level_values(0)

            # CLEANING
            df.dropna(subset=['open','high','low','close','volume'], inplace=True)
            df = df[df['volume'] > 0]
            df[['open','high','low','close']] = (
                df[['open','high','low','close']]
                .astype(float)
                .round(2)
            )
            df.drop_duplicates(subset=['date'], inplace=True)

            # tag & format
            df['symbol'] = sym
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')

            rows += df.to_dict(orient='records')

        return rows

    @task
    def create_raw_table():
        hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
        conn = hook.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("USE DATABASE COUNTRY")
            cursor.execute("USE SCHEMA RAW")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_prices (
                    date DATE,
                    open FLOAT,
                    high FLOAT,
                    low FLOAT,
                    close FLOAT,
                    volume BIGINT,
                    symbol VARCHAR,
                    PRIMARY KEY (date, symbol)
                );
            """)
        finally:
            cursor.close()
            conn.close()

    @task
    def load_data(rows):
        hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
        conn = hook.get_conn()
        cursor = conn.cursor()

        # cutoff for 180-day window
        cutoff = (datetime.utcnow() - timedelta(days=180)).strftime('%Y-%m-%d')

        try:
            cursor.execute("USE DATABASE COUNTRY")
            cursor.execute("USE SCHEMA RAW")

            # wrap DELETE + INSERT in a single transaction
            cursor.execute("BEGIN")

            # delete existing rows in window for idempotency
            cursor.execute(
                "DELETE FROM stock_prices WHERE date >= %s",
                (cutoff,)
            )

            # bulk insert fresh, cleaned data
            insert_sql = """
                INSERT INTO stock_prices
                  (date, open, high, low, close, volume, symbol)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            for r in rows:
                cursor.execute(insert_sql, (
                    r['date'],
                    r['open'],
                    r['high'],
                    r['low'],
                    r['close'],
                    int(r['volume']),
                    r['symbol']
                ))

            cursor.execute("COMMIT")

        except Exception:
            cursor.execute("ROLLBACK")
            raise

        finally:
            cursor.close()
            conn.close()

    # define DAG dependencies
    stock_rows = fetch_stock_data()
    create_raw_table()
    load_data(stock_rows)
