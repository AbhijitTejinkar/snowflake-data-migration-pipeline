-- ================================================
-- Snowflake Data Migration Validation Queries
-- ================================================

-- 1. Row count reconciliation
SELECT
    (SELECT COUNT(*) FROM STAGING.STG_SALES)   AS source_count,
    (SELECT COUNT(*) FROM CURATED.SALES)       AS target_count,
    CASE
        WHEN (SELECT COUNT(*) FROM STAGING.STG_SALES) =
             (SELECT COUNT(*) FROM CURATED.SALES)
        THEN 'PASS' ELSE 'FAIL'
    END AS reconciliation_status;

-- 2. Null check on key columns
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_ids,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_ids
FROM CURATED.SALES;

-- 3. Duplicate check
SELECT order_id, COUNT(*) AS duplicate_count
FROM CURATED.SALES
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 4. Referential integrity check
SELECT COUNT(*) AS orphan_records
FROM CURATED.SALES s
LEFT JOIN CURATED.CUSTOMERS c ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- 5. Aggregated summary table creation
CREATE OR REPLACE TABLE CURATED.SALES_SUMMARY AS
SELECT
    year,
    month,
    status,
    COUNT(*) AS order_count,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value
FROM CURATED.SALES
GROUP BY year, month, status;