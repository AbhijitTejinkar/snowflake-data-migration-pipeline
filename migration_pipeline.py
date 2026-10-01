import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Snowflake connection
def get_snowflake_connection():
    return snowflake.connector.connect(
        user='YOUR_USER',
        password='YOUR_PASSWORD',
        account='YOUR_ACCOUNT',
        warehouse='COMPUTE_WH',
        database='ANALYTICS',
        schema='CURATED',
        role='DATA_ENGINEER'
    )

def load_staging_data(conn, source_file):
    """Load data from CSV into Snowflake staging table."""
    df = pd.read_csv(source_file)
    success, nchunks, nrows, _ = write_pandas(conn, df, 'STG_SALES')
    logging.info(f"Loaded {nrows} rows into STG_SALES")
    return nrows

def apply_transformations(conn):
    """Apply transformation and validation logic."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CURATED.SALES
        SELECT
            order_id,
            customer_id,
            TO_DATE(order_date, 'YYYY-MM-DD') AS order_date,
            CAST(amount AS DECIMAL(12,2)) AS amount,
            UPPER(TRIM(status)) AS status,
            YEAR(order_date) AS year,
            MONTH(order_date) AS month
        FROM STAGING.STG_SALES
        WHERE order_id IS NOT NULL
          AND customer_id IS NOT NULL
          AND amount > 0
        QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY loaded_at DESC) = 1
    """)
    logging.info(f"Inserted {cursor.rowcount} rows into CURATED.SALES")
    cursor.close()

def run_reconciliation(conn):
    """Source-to-target reconciliation checks."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM STAGING.STG_SALES) AS source_count,
            (SELECT COUNT(*) FROM CURATED.SALES) AS target_count
    """)
    result = cursor.fetchone()
    logging.info(f"Source rows: {result[0]}, Target rows: {result[1]}")
    if result[0] != result[1]:
        logging.warning("Row count mismatch detected - investigate immediately")
    cursor.close()

if __name__ == "__main__":
    conn = get_snowflake_connection()
    try:
        load_staging_data(conn, 'data/source_sales.csv')
        apply_transformations(conn)
        run_reconciliation(conn)
        logging.info("Migration pipeline completed successfully")
    finally:
        conn.close()