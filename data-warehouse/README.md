# Retail Data Warehouse on Databricks

A **YouTube-ready teaching project** for students: build a complete retail data warehouse using the **medallion architecture** (Bronze → Silver → Gold) and a **star schema**.

- **Workspace:** https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022
- **GitHub:** https://github.com/akhilvydyula01/databricks
- **Notebooks path in workspace:** `notebooks/data_warehouse/`

## What students will learn

1. Lakehouse + medallion architecture
2. Ingest raw retail data to **Bronze**
3. Clean / conform data in **Silver**
4. Build a **Gold star schema** (facts + dimensions)
5. Implement **SCD Type 2** for customers
6. Run **data quality** checks
7. Answer business questions with **SQL analytics**
8. Wire an **end-to-end pipeline**

## Domain

Fictional retailer **NovaMart**:
- Customers, products, stores, and sales orders
- Sample data is generated inside the notebooks (no external download needed)

## Run order (for class / YouTube)

| # | Notebook | Purpose | Est. time on video |
|---|----------|---------|--------------------|
| 00 | `00_architecture_overview` | Architecture + teaching map | 5–8 min |
| 01 | `01_setup_and_sample_data` | Catalog/schema + generate raw files | 8–10 min |
| 02 | `02_bronze_ingestion` | Land raw data as Bronze tables | 8–10 min |
| 03 | `03_silver_transform` | Clean, type, dedupe | 10–12 min |
| 04 | `04_gold_star_schema` | dims + fact_sales | 12–15 min |
| 05 | `05_scd2_customers` | Slowly Changing Dimension Type 2 | 10–12 min |
| 06 | `06_data_quality` | Expectations / quarantine | 8–10 min |
| 07 | `07_analytics_sql` | Business questions + KPIs | 10–12 min |
| 08 | `08_end_to_end_pipeline` | One-click full refresh demo | 5–8 min |

Full presenter script: [`YOUTUBE_TEACHING_GUIDE.md`](./YOUTUBE_TEACHING_GUIDE.md)

## How to open in Databricks

1. Workspace → **Repos** → Add Git folder  
   `https://github.com/akhilvydyula01/databricks`
2. **Pull** latest
3. Open `notebooks/data_warehouse/00_architecture_overview`
4. Attach any **DBR 13+** cluster (Photon optional) → Run All

## Architecture (talking point)

```text
Source (CSV/JSON files)
        │
        ▼
   Bronze (raw)     ← append / land as-is + metadata
        │
        ▼
   Silver (clean)   ← typed, deduped, conformed
        │
        ▼
   Gold (star)      ← dim_date, dim_customer, dim_product, dim_store, fact_sales
        │
        ▼
   Analytics / BI   ← SQL KPIs, dashboards, student exercises
```
