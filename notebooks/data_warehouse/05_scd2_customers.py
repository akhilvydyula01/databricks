# Databricks notebook source
# MAGIC %md
# MAGIC # 05 — SCD Type 2 (Customers)
# MAGIC Track customer attribute history with `valid_from`, `valid_to`, `is_current`.

# COMMAND ----------

from pyspark.sql import functions as F
from delta.tables import DeltaTable

SCHEMA_NAME = "retail_dwh"
spark.sql(f"USE {SCHEMA_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initialize SCD2 table from current Silver customers

# COMMAND ----------

scd2 = (
    spark.table(f"{SCHEMA_NAME}.silver_customers")
    .select(
        F.monotonically_increasing_id().alias("customer_sk"),
        "customer_id",
        "full_name",
        "email",
        "city",
        "state",
        "segment",
        "signup_date",
        F.lit(F.current_date()).alias("valid_from"),
        F.lit(None).cast("date").alias("valid_to"),
        F.lit(True).alias("is_current"),
    )
)
scd2.write.mode("overwrite").format("delta").saveAsTable(f"{SCHEMA_NAME}.gold_dim_customer_scd2")
display(spark.table(f"{SCHEMA_NAME}.gold_dim_customer_scd2"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Simulate source changes (teaching demo)
# MAGIC - Customer 101 moves Austin → Houston
# MAGIC - Customer 104 segment HOME_OFFICE → CORPORATE

# COMMAND ----------

updates = spark.createDataFrame(
    [
        (101, "Aisha Khan", "aisha@example.com", "Houston", "TX", "CONSUMER", "2023-01-10"),
        (104, "Diya Patel", "diya@example.com", "Chicago", "IL", "CORPORATE", "2023-03-01"),
    ],
    "customer_id INT, full_name STRING, email STRING, city STRING, state STRING, segment STRING, signup_date STRING",
).withColumn("signup_date", F.to_date("signup_date"))

# Incoming snapshot = unchanged customers + updates
unchanged = (
    spark.table(f"{SCHEMA_NAME}.silver_customers")
    .filter(~F.col("customer_id").isin(101, 104))
    .select("customer_id", "full_name", "email", "city", "state", "segment", "signup_date")
)
incoming = unchanged.unionByName(updates)
display(incoming.filter(F.col("customer_id").isin(101, 104)))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Apply SCD2 MERGE pattern

# COMMAND ----------

target = DeltaTable.forName(spark, f"{SCHEMA_NAME}.gold_dim_customer_scd2")

# 1) Close current rows that changed
changed = (
    incoming.alias("i")
    .join(
        spark.table(f"{SCHEMA_NAME}.gold_dim_customer_scd2").alias("t"),
        on="customer_id",
        how="inner",
    )
    .filter(F.col("t.is_current") == True)
    .filter(
        (F.col("i.city") != F.col("t.city"))
        | (F.col("i.state") != F.col("t.state"))
        | (F.col("i.segment") != F.col("t.segment"))
        | (F.col("i.full_name") != F.col("t.full_name"))
        | (F.col("i.email") != F.col("t.email"))
    )
    .select("i.customer_id")
)

target.alias("t").merge(
    changed.alias("c"),
    "t.customer_id = c.customer_id AND t.is_current = true",
).whenMatchedUpdate(
    set={
        "is_current": F.lit(False),
        "valid_to": F.current_date(),
    }
).execute()

# 2) Insert new current versions for changed + brand-new customers
existing_current = spark.table(f"{SCHEMA_NAME}.gold_dim_customer_scd2").filter("is_current = true")
to_insert = (
    incoming.alias("i")
    .join(existing_current.alias("e"), on="customer_id", how="left_anti")
    .select(
        F.monotonically_increasing_id().alias("customer_sk"),
        "customer_id",
        "full_name",
        "email",
        "city",
        "state",
        "segment",
        "signup_date",
        F.current_date().alias("valid_from"),
        F.lit(None).cast("date").alias("valid_to"),
        F.lit(True).alias("is_current"),
    )
)

to_insert.write.mode("append").format("delta").saveAsTable(f"{SCHEMA_NAME}.gold_dim_customer_scd2")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id, full_name, city, segment, valid_from, valid_to, is_current
# MAGIC FROM retail_dwh.gold_dim_customer_scd2
# MAGIC WHERE customer_id IN (101, 104)
# MAGIC ORDER BY customer_id, valid_from

# COMMAND ----------

# MAGIC %md
# MAGIC ### Teaching checkpoint
# MAGIC - SCD1 overwrites history; SCD2 **preserves** it.
# MAGIC - Fact tables should join the version valid on `order_date` in advanced designs.
# MAGIC - Ask students: what breaks if we only keep `is_current = true`?
