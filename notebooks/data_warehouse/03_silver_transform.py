# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Silver Transform
# MAGIC Clean, cast types, standardize, and deduplicate into trusted Silver tables.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

SCHEMA_NAME = "retail_dwh"
spark.sql(f"USE {SCHEMA_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Customers / products / stores

# COMMAND ----------

silver_customers = (
    spark.table(f"{SCHEMA_NAME}.bronze_customers")
    .select(
        F.col("customer_id").cast("int").alias("customer_id"),
        F.trim("full_name").alias("full_name"),
        F.lower(F.trim("email")).alias("email"),
        F.trim("city").alias("city"),
        F.upper(F.trim("state")).alias("state"),
        F.upper(F.trim("segment")).alias("segment"),
        F.to_date("signup_date").alias("signup_date"),
        F.col("_ingested_at"),
    )
    .dropDuplicates(["customer_id"])
)

silver_products = (
    spark.table(f"{SCHEMA_NAME}.bronze_products")
    .select(
        F.col("product_id").cast("int").alias("product_id"),
        F.trim("product_name").alias("product_name"),
        F.trim("category").alias("category"),
        F.trim("subcategory").alias("subcategory"),
        F.col("unit_price").cast("double").alias("unit_price"),
        F.col("_ingested_at"),
    )
    .dropDuplicates(["product_id"])
)

silver_stores = (
    spark.table(f"{SCHEMA_NAME}.bronze_stores")
    .select(
        F.col("store_id").cast("int").alias("store_id"),
        F.trim("store_name").alias("store_name"),
        F.trim("city").alias("city"),
        F.upper(F.trim("state")).alias("state"),
        F.trim("region").alias("region"),
        F.col("_ingested_at"),
    )
    .dropDuplicates(["store_id"])
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Orders — cast, filter invalid amounts, dedupe by latest ingest

# COMMAND ----------

orders_typed = (
    spark.table(f"{SCHEMA_NAME}.bronze_orders")
    .select(
        F.col("order_id").cast("int").alias("order_id"),
        F.to_date("order_date").alias("order_date"),
        F.col("customer_id").cast("int").alias("customer_id"),
        F.col("product_id").cast("int").alias("product_id"),
        F.col("store_id").cast("int").alias("store_id"),
        F.col("quantity").cast("int").alias("quantity"),
        F.col("amount").cast("double").alias("amount"),
        F.lower(F.trim("payment_method")).alias("payment_method"),
        F.col("_ingested_at"),
    )
)

# Keep rejected rows for quality teaching
rejected_orders = orders_typed.filter(
    (F.col("order_id").isNull())
    | (F.col("order_date").isNull())
    | (F.col("quantity") <= 0)
    | (F.col("amount") <= 0)
).withColumn("reject_reason", F.lit("invalid_order_fields"))

valid_orders = orders_typed.filter(
    F.col("order_id").isNotNull()
    & F.col("order_date").isNotNull()
    & (F.col("quantity") > 0)
    & (F.col("amount") > 0)
)

w = Window.partitionBy("order_id").orderBy(F.col("_ingested_at").desc())
silver_orders = (
    valid_orders.withColumn("rn", F.row_number().over(w))
    .filter(F.col("rn") == 1)
    .drop("rn")
)

silver_customers.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.silver_customers")
silver_products.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.silver_products")
silver_stores.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.silver_stores")
silver_orders.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.silver_orders")
rejected_orders.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.silver_orders_rejected")

print("Silver customers:", silver_customers.count())
print("Silver orders:", silver_orders.count())
print("Rejected orders:", rejected_orders.count())

# COMMAND ----------

display(spark.table(f"{SCHEMA_NAME}.silver_orders_rejected"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT payment_method, COUNT(*) AS orders, ROUND(SUM(amount), 2) AS revenue
# MAGIC FROM retail_dwh.silver_orders
# MAGIC GROUP BY payment_method
# MAGIC ORDER BY revenue DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Teaching checkpoint
# MAGIC - Silver is where **trust** is created.
# MAGIC - Rejected rows are not deleted from the lake story — we keep them in a reject table.
# MAGIC - Dedupe key for orders in this demo: `order_id`.
