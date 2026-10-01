# Snowflake Data Migration & Validation Pipeline

## Project Overview
Enterprise-grade data migration pipeline that moves legacy on-premises and cloud data into Snowflake, applying transformation logic, validation, and reconciliation to ensure 99.9% data accuracy with zero production downtime.

## Architecture

Source Systems → S3/Local Staging → Snowflake Stage → COPY INTO → Transformation Layer → Curated Tables → Power BI

## Tech Stack
- Snowflake
- SQL
- Python
- AWS S3 (staging)
- Snowflake Stages and COPY INTO
- Power BI
- Git

## Key Features
- End-to-end data migration from legacy systems to Snowflake
- Source-to-target validation and reconciliation
- Data quality checks (nulls, duplicates, referential integrity)
- Optimized aggregation and summary tables
- Incremental loading with MERGE statements
- Snowflake time travel and cloning for safe rollback
- Production deployment with client approval workflow
- Power BI reporting enablement

## Results
- Migrated 100+ TB of legacy retail data
- Achieved 99.9% data accuracy
- Reduced manual processing effort by 40%
- Improved downstream Power BI performance by up to 3x
- Sustained 99.5%+ pipeline uptime

## How to Run
1. Stage source data in S3 or local
2. COPY INTO Snowflake staging tables
3. Apply transformation and validation logic
4. Merge into curated tables
5. Run reconciliation queries
6. Connect Power BI to curated layer

## Author
Abhijit Tejinkar — Senior Data Engineer
