# YouTube Teaching Guide — Databricks Retail Data Warehouse

Use this as your **video script outline**. Total target length: **70–90 minutes** (or split into a playlist).

## Video title ideas

- Build a Complete Data Warehouse in Databricks (Bronze–Silver–Gold)
- Databricks Medallion Architecture + Star Schema for Beginners
- Teach Retail DWH on Databricks: SCD2, Quality Checks & SQL Analytics

## Hook (0:00–1:00)

> “Today we build a real retail data warehouse in Databricks — from raw files to analytics-ready star schema — the same pattern used in industry lakehouses.”

Show the architecture diagram from notebook `00`.

## Chapter map

### Part 1 — Why lakehouse / medallion (Notebook 00)
**Say:** Batch warehouses used to be rigid. Lakehouse keeps cheap storage + warehouse performance. Medallion (Bronze/Silver/Gold) keeps raw history while delivering clean marts.

**Show:** Architecture cell + table naming convention `retail_dwh.bronze_*`.

### Part 2 — Project setup + sample data (Notebook 01)
**Say:** We create schema `retail_dwh` and generate NovaMart customer/product/store/order files so students can reproduce without downloads.

**Do:** Run All → show files under the landing path.

**Ask students:** Why keep raw landing files if we already have tables?

### Part 3 — Bronze ingestion (Notebook 02)
**Say:** Bronze is “as landed.” We add `_ingested_at` and `_source_file` for lineage.

**Do:** Create `bronze_customers`, `bronze_products`, `bronze_stores`, `bronze_orders`.
**Show:** `display(spark.table(...))` with messy types / nulls still present.

### Part 4 — Silver transforms (Notebook 03)
**Say:** Silver is trusted enterprise data: cast types, standardize columns, drop bad rows, dedupe.

**Do:** Build `silver_*` tables with `MERGE` or overwrite for teaching clarity.
**Student challenge:** Add email lowercase standardization.

### Part 5 — Gold star schema (Notebook 04)
**Say:** Analysts think in facts and dimensions. We build:
- `dim_date`, `dim_customer`, `dim_product`, `dim_store`
- `fact_sales` with surrogate keys + measures

**Draw on screen:** star with `fact_sales` in the center.

### Part 6 — SCD Type 2 (Notebook 05)
**Say:** Customer city/segment changes over time. SCD2 keeps history with `valid_from`, `valid_to`, `is_current`.

**Do:** Apply an address change and show two versions for one customer.

### Part 7 — Data quality (Notebook 06)
**Say:** Warehouses fail silently without tests. We assert PK uniqueness, not-null amounts, referential integrity, and quarantine bad records.

### Part 8 — Analytics SQL (Notebook 07)
**Say:** This is the business payoff.
Run:
- Revenue by month
- Top products
- Store performance
- Customer segment contribution

**Student exercise:** “Which store has the highest average order value?”

### Part 9 — End-to-end pipeline (Notebook 08)
**Say:** In production this becomes a Databricks Job / DLT pipeline. Today we call each stage in order for a full refresh demo.

## Closing (last 2 minutes)

Recap:
1. Medallion separates raw vs trusted vs serving
2. Star schema serves BI
3. SCD2 preserves history
4. Quality gates protect Gold

CTA: “Clone the public repo, Pull in Repos, run notebooks 00→08.”

## Playlist split (optional)

1. Ep1: Architecture + Bronze (00–02)
2. Ep2: Silver + Gold (03–04)
3. Ep3: SCD2 + Quality (05–06)
4. Ep4: Analytics + Pipeline (07–08)

## Classroom exercises

1. Add a new source: `returns.csv` → bronze → silver → `fact_returns`
2. Add `dim_promotion`
3. Build a dashboard in Databricks SQL on `gold_fact_sales`
4. Convert notebook 08 into a scheduled Job
