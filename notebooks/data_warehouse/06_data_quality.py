# Databricks notebook source
# MAGIC %md
# MAGIC # 06 — Data Quality Gates
# MAGIC Fail fast on warehouse rules before publishing Gold to analysts.

# COMMAND ----------

from pyspark.sql import functions as F

SCHEMA_NAME = "retail_dwh"
spark.sql(f"USE {SCHEMA_NAME}")
results = []


def check(name: str, passed: bool, details: str):
    results.append((name, passed, details))
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name} — {details}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Core expectations

# COMMAND ----------

fact = spark.table(f"{SCHEMA_NAME}.gold_fact_sales")
dim_c = spark.table(f"{SCHEMA_NAME}.gold_dim_customer")
dim_p = spark.table(f"{SCHEMA_NAME}.gold_dim_product")
dim_s = spark.table(f"{SCHEMA_NAME}.gold_dim_store")
rejected = spark.table(f"{SCHEMA_NAME}.silver_orders_rejected")

# 1) Fact PK uniqueness
pk_dupes = fact.groupBy("sales_key").count().filter("count > 1").count()
check("fact_sales_pk_unique", pk_dupes == 0, f"duplicate sales_key rows={pk_dupes}")

# 2) Measures must be positive
bad_measures = fact.filter((F.col("quantity") <= 0) | (F.col("gross_amount") <= 0)).count()
check("fact_measures_positive", bad_measures == 0, f"bad measure rows={bad_measures}")

# 3) Dimension PK uniqueness
for label, df, colname in [
    ("dim_customer_pk", dim_c, "customer_sk"),
    ("dim_product_pk", dim_p, "product_sk"),
    ("dim_store_pk", dim_s, "store_sk"),
]:
    d = df.groupBy(colname).count().filter("count > 1").count()
    check(label, d == 0, f"duplicate {colname}={d}")

# 4) Orphan keys (referential integrity)
orphans = (
    fact.join(dim_c, "customer_sk", "left_anti").count()
    + fact.join(dim_p, "product_sk", "left_anti").count()
    + fact.join(dim_s, "store_sk", "left_anti").count()
)
check("fact_no_orphan_keys", orphans == 0, f"orphan joins={orphans}")

# 5) Reject table should capture known bad amount row
check("reject_table_has_rows", rejected.count() >= 1, f"rejected_rows={rejected.count()}")

# COMMAND ----------

dq = spark.createDataFrame(results, "rule_name STRING, passed BOOLEAN, details STRING").withColumn(
    "checked_at", F.current_timestamp()
)
dq.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.dq_results")
display(dq)

failed = dq.filter("passed = false").count()
if failed:
    raise Exception(f"{failed} data quality rule(s) failed. See retail_dwh.dq_results")
else:
    print("All data quality checks passed.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Teaching checkpoint
# MAGIC - Quality gates belong **before** dashboard publish.
# MAGIC - Store results historically in production (append + run_id).
# MAGIC - Student stretch: add a freshness check (`max(order_date)`).
