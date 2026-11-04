# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — Bronze Ingestion
# MAGIC Land raw files **as-is** into Bronze tables and add lineage columns.

# COMMAND ----------

from pyspark.sql import functions as F

SCHEMA_NAME = "retail_dwh"
LANDING_PATH = spark.table(f"{SCHEMA_NAME}.project_config").collect()[0]["landing_path"]
spark.sql(f"USE {SCHEMA_NAME}")
print("Landing path:", LANDING_PATH)

# COMMAND ----------

def to_bronze(df, source_name: str):
    return (
        df.withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_system", F.lit("novamart_files"))
        .withColumn("_source_name", F.lit(source_name))
    )


bronze_customers = to_bronze(
    spark.read.option("header", True).csv(f"{LANDING_PATH}/customers"),
    "customers",
)
bronze_products = to_bronze(
    spark.read.option("header", True).csv(f"{LANDING_PATH}/products"),
    "products",
)
bronze_stores = to_bronze(
    spark.read.option("header", True).csv(f"{LANDING_PATH}/stores"),
    "stores",
)
bronze_orders = to_bronze(
    spark.read.json(f"{LANDING_PATH}/orders"),
    "orders",
)

bronze_customers.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.bronze_customers")
bronze_products.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.bronze_products")
bronze_stores.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.bronze_stores")
bronze_orders.write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.bronze_orders")

print("Bronze tables created.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Inspect Bronze (show students the raw shape)

# COMMAND ----------

print("bronze_orders schema:")
spark.table(f"{SCHEMA_NAME}.bronze_orders").printSchema()
display(spark.table(f"{SCHEMA_NAME}.bronze_orders").limit(10))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT _source_name, COUNT(*) AS row_count
# MAGIC FROM retail_dwh.bronze_orders
# MAGIC GROUP BY _source_name
# MAGIC UNION ALL
# MAGIC SELECT 'bronze_customers', COUNT(*) FROM retail_dwh.bronze_customers
# MAGIC UNION ALL
# MAGIC SELECT 'bronze_products', COUNT(*) FROM retail_dwh.bronze_products
# MAGIC UNION ALL
# MAGIC SELECT 'bronze_stores', COUNT(*) FROM retail_dwh.bronze_stores

# COMMAND ----------

# MAGIC %md
# MAGIC ### Teaching checkpoint
# MAGIC - Bronze keeps history of what arrived.
# MAGIC - We do **not** fix business rules here (that is Silver).
# MAGIC - Lineage columns help debugging in production.
