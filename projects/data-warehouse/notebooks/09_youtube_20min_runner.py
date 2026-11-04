# Databricks notebook source
# MAGIC %md
# MAGIC # 09 — YouTube 20-Minute Demo Runner
# MAGIC Fast path for recording. Runs core stages, then shows KPI + SCD2 highlight.
# MAGIC Full teaching script: `learning-resources/guides/YOUTUBE_20MIN_DEMO.md`

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1) Run core pipeline notebooks

# COMMAND ----------

import datetime as dt

notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
base = notebook_path.rsplit("/", 1)[0]

steps = [
    "01_setup_and_sample_data",
    "02_bronze_ingestion",
    "03_silver_transform",
    "04_gold_star_schema",
    "05_scd2_customers",
    "06_data_quality",
]

for step in steps:
    print(f"Running {step} @ {dt.datetime.utcnow().isoformat()}Z")
    dbutils.notebook.run(f"{base}/{step}", timeout_seconds=1800)
    print(f"Done {step}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2) On-camera KPI payoff

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS orders, ROUND(SUM(gross_amount), 2) AS revenue, ROUND(AVG(gross_amount), 2) AS aov
# MAGIC FROM retail_dwh.gold_fact_sales

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT d.month_name, ROUND(SUM(f.gross_amount), 2) AS revenue
# MAGIC FROM retail_dwh.gold_fact_sales f
# MAGIC JOIN retail_dwh.gold_dim_date d ON f.date_key = d.date_key
# MAGIC GROUP BY d.month, d.month_name
# MAGIC ORDER BY d.month

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3) SCD2 highlight (customer moves)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id, city, segment, valid_from, valid_to, is_current
# MAGIC FROM retail_dwh.gold_dim_customer_scd2
# MAGIC WHERE customer_id IN (101, 104)
# MAGIC ORDER BY customer_id, valid_from

# COMMAND ----------

# MAGIC %md
# MAGIC ## CTA for viewers
# MAGIC - Repo: https://github.com/akhilvydyula01/databricks
# MAGIC - Assignment: `learning-resources/assignments/STUDENT_ASSIGNMENT.md`
# MAGIC - Next video: Databricks Job + Returns fact table

# COMMAND ----------

print("20-minute demo data is ready. Switch to SQL cells for on-camera payoff.")
