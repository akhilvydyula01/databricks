# Databricks notebook source
# MAGIC %md
# MAGIC # 08 — End-to-End Pipeline (Full Refresh Demo)
# MAGIC Runs the warehouse stages in order for a classroom / YouTube finale.
# MAGIC
# MAGIC In production, convert this to a **Databricks Job** with task dependencies.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Pipeline map
# MAGIC 1. Setup + sample data
# MAGIC 2. Bronze ingestion
# MAGIC 3. Silver transform
# MAGIC 4. Gold star schema
# MAGIC 5. SCD2 customers
# MAGIC 6. Data quality gate
# MAGIC 7. Analytics smoke test

# COMMAND ----------

import datetime as dt

# Resolve notebook directory so this works from Databricks Repos / Git folders
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
base = notebook_path.rsplit("/", 1)[0]
print("Notebook base:", base)

steps = [
    "01_setup_and_sample_data",
    "02_bronze_ingestion",
    "03_silver_transform",
    "04_gold_star_schema",
    "05_scd2_customers",
    "06_data_quality",
]

run_log = []
for step in steps:
    path = f"{base}/{step}"
    print(f"\n=== Running {step} ===")
    started = dt.datetime.utcnow()
    result = dbutils.notebook.run(path, timeout_seconds=1800)
    ended = dt.datetime.utcnow()
    run_log.append((step, "SUCCESS", str(started), str(ended), result or ""))
    print(f"Finished {step}")

# COMMAND ----------

# Smoke analytics
spark.sql("USE retail_dwh")
kpi = spark.sql(
    """
    SELECT COUNT(*) AS orders, ROUND(SUM(gross_amount), 2) AS revenue
    FROM gold_fact_sales
    """
)
display(kpi)
display(spark.createDataFrame(run_log, "step STRING, status STRING, started_at STRING, ended_at STRING, notebook_result STRING"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Production next steps for students
# MAGIC - Create a Databricks **Job** with the same task order
# MAGIC - Schedule hourly/daily
# MAGIC - Add email / Slack alerts on quality failure
# MAGIC - Replace sample files with Autoloader from cloud storage
# MAGIC - Upgrade Gold to Unity Catalog + Databricks SQL dashboard
# MAGIC
# MAGIC Repo: https://github.com/akhilvydyula01/databricks

# COMMAND ----------

print("End-to-end retail data warehouse pipeline completed.")
