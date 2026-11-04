# Databricks notebook source
# MAGIC %md
# MAGIC # 00 — Architecture Overview (Teaching Intro)
# MAGIC **NovaMart Retail Data Warehouse** on Databricks
# MAGIC
# MAGIC Use this notebook at the start of your YouTube lesson / class.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Learning goals
# MAGIC 1. Explain **lakehouse** vs classic warehouse
# MAGIC 2. Explain **medallion architecture**: Bronze → Silver → Gold
# MAGIC 3. Explain **star schema** for analytics
# MAGIC 4. Preview the notebook path students will run

# COMMAND ----------

# MAGIC %md
# MAGIC ## Architecture
# MAGIC
# MAGIC ```text
# MAGIC  CSV/JSON landing files
# MAGIC           │
# MAGIC           ▼
# MAGIC   ┌───────────────────┐
# MAGIC   │  BRONZE (raw)     │  append-friendly, lineage columns
# MAGIC   └─────────┬─────────┘
# MAGIC             ▼
# MAGIC   ┌───────────────────┐
# MAGIC   │  SILVER (clean)   │  typed, deduped, conformed
# MAGIC   └─────────┬─────────┘
# MAGIC             ▼
# MAGIC   ┌───────────────────┐
# MAGIC   │  GOLD (star)      │  dims + fact_sales for BI
# MAGIC   └─────────┬─────────┘
# MAGIC             ▼
# MAGIC        SQL Analytics / Dashboards
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## Star schema (Gold)
# MAGIC
# MAGIC ```text
# MAGIC             dim_date
# MAGIC                │
# MAGIC dim_customer ──┼── dim_product
# MAGIC                │
# MAGIC            fact_sales
# MAGIC                │
# MAGIC            dim_store
# MAGIC ```
# MAGIC
# MAGIC **Fact:** `fact_sales` (grain = one order line)
# MAGIC **Dimensions:** customer, product, store, date

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table naming convention
# MAGIC
# MAGIC | Layer | Example table |
# MAGIC |-------|----------------|
# MAGIC | Bronze | `retail_dwh.bronze_orders` |
# MAGIC | Silver | `retail_dwh.silver_orders` |
# MAGIC | Gold | `retail_dwh.gold_fact_sales` |
# MAGIC | Gold | `retail_dwh.gold_dim_customer` |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run order for students
# MAGIC 1. `01_setup_and_sample_data`
# MAGIC 2. `02_bronze_ingestion`
# MAGIC 3. `03_silver_transform`
# MAGIC 4. `04_gold_star_schema`
# MAGIC 5. `05_scd2_customers`
# MAGIC 6. `06_data_quality`
# MAGIC 7. `07_analytics_sql`
# MAGIC 8. `08_end_to_end_pipeline`
# MAGIC
# MAGIC Repo: https://github.com/akhilvydyula01/databricks

# COMMAND ----------

print("Architecture intro ready. Continue to notebook 01_setup_and_sample_data.")
