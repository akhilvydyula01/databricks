# Databricks notebook source
# MAGIC %md
# MAGIC # 04 — Gold Star Schema
# MAGIC Build analytics-ready dimensions and `gold_fact_sales`.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import DateType
import datetime as dt

SCHEMA_NAME = "retail_dwh"
spark.sql(f"USE {SCHEMA_NAME}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## dim_date

# COMMAND ----------

start = dt.date(2024, 1, 1)
end = dt.date(2024, 12, 31)
days = (end - start).days
date_df = (
    spark.range(0, days + 1)
    .withColumn("order_date", F.date_add(F.lit(start.isoformat()).cast(DateType()), F.col("id").cast("int")))
    .select(
        F.date_format("order_date", "yyyyMMdd").cast("int").alias("date_key"),
        F.col("order_date"),
        F.year("order_date").alias("year"),
        F.quarter("order_date").alias("quarter"),
        F.month("order_date").alias("month"),
        F.date_format("order_date", "MMMM").alias("month_name"),
        F.dayofweek("order_date").alias("day_of_week"),
        F.date_format("order_date", "E").alias("day_name"),
        F.when(F.dayofweek("order_date").isin(1, 7), F.lit(True)).otherwise(F.lit(False)).alias("is_weekend"),
    )
)
date_df.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.gold_dim_date")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Dimensions from Silver

# COMMAND ----------

dim_customer = (
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
        F.current_timestamp().alias("effective_ts"),
    )
)

dim_product = (
    spark.table(f"{SCHEMA_NAME}.silver_products")
    .select(
        F.monotonically_increasing_id().alias("product_sk"),
        "product_id",
        "product_name",
        "category",
        "subcategory",
        "unit_price",
    )
)

dim_store = (
    spark.table(f"{SCHEMA_NAME}.silver_stores")
    .select(
        F.monotonically_increasing_id().alias("store_sk"),
        "store_id",
        "store_name",
        "city",
        "state",
        "region",
    )
)

dim_customer.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.gold_dim_customer")
dim_product.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.gold_dim_product")
dim_store.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.gold_dim_store")

# COMMAND ----------

# MAGIC %md
# MAGIC ## fact_sales (grain = one order line / order_id in this demo)

# COMMAND ----------

fact = (
    spark.table(f"{SCHEMA_NAME}.silver_orders").alias("o")
    .join(spark.table(f"{SCHEMA_NAME}.gold_dim_customer").alias("c"), on="customer_id", how="inner")
    .join(spark.table(f"{SCHEMA_NAME}.gold_dim_product").alias("p"), on="product_id", how="inner")
    .join(spark.table(f"{SCHEMA_NAME}.gold_dim_store").alias("s"), on="store_id", how="inner")
    .join(
        spark.table(f"{SCHEMA_NAME}.gold_dim_date").alias("d"),
        on="order_date",
        how="inner",
    )
    .select(
        F.col("o.order_id").alias("sales_key"),
        F.col("d.date_key"),
        F.col("c.customer_sk"),
        F.col("p.product_sk"),
        F.col("s.store_sk"),
        F.col("o.order_date"),
        F.col("o.quantity"),
        F.col("o.amount").alias("gross_amount"),
        (F.col("o.amount") / F.col("o.quantity")).alias("unit_amount"),
        F.col("o.payment_method"),
        F.current_timestamp().alias("loaded_at"),
    )
)

fact.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.gold_fact_sales")
print("Fact rows:", fact.count())
display(fact.limit(10))

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_dwh LIKE 'gold_*'

# COMMAND ----------

# MAGIC %md
# MAGIC ### Teaching checkpoint
# MAGIC - Surrogate keys (`*_sk`) protect history when natural keys change.
# MAGIC - Fact grain must be stated clearly: here one row per `order_id`.
# MAGIC - Next notebook upgrades customer dimension to **SCD Type 2**.
