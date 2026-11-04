# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Setup & Sample Data
# MAGIC Creates schema `retail_dwh` and generates NovaMart landing files for the class.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import *
import datetime as dt

SCHEMA_NAME = "retail_dwh"
LANDING_PATH = "/FileStore/retail_dwh/landing"

spark.sql(f"CREATE DATABASE IF NOT EXISTS {SCHEMA_NAME}")
spark.sql(f"USE {SCHEMA_NAME}")
dbutils.fs.mkdirs(LANDING_PATH)
print(f"Schema: {SCHEMA_NAME}")
print(f"Landing path: {LANDING_PATH}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate dimensional source data

# COMMAND ----------

customers = spark.createDataFrame(
    [
        (101, "Aisha Khan", "aisha@example.com", "Austin", "TX", "CONSUMER", "2023-01-10"),
        (102, "Ben Ortiz", "ben@example.com", "Dallas", "TX", "CORPORATE", "2023-02-02"),
        (103, "Chen Wei", "chen@example.com", "Seattle", "WA", "CONSUMER", "2023-02-18"),
        (104, "Diya Patel", "diya@example.com", "Chicago", "IL", "HOME_OFFICE", "2023-03-01"),
        (105, "Eli Brown", "eli@example.com", "Austin", "TX", "CONSUMER", "2023-03-12"),
        (106, "Fatima Noor", "fatima@example.com", "New York", "NY", "CORPORATE", "2023-04-05"),
        (107, "Gabe Lopez", "gabe@example.com", "Miami", "FL", "CONSUMER", "2023-04-20"),
        (108, "Hana Suzuki", "hana@example.com", "Seattle", "WA", "HOME_OFFICE", "2023-05-03"),
    ],
    "customer_id INT, full_name STRING, email STRING, city STRING, state STRING, segment STRING, signup_date STRING",
)

products = spark.createDataFrame(
    [
        (1001, "Nova Laptop 14", "Electronics", "Computers", 899.00),
        (1002, "NoiseCancel Headset", "Electronics", "Audio", 149.00),
        (1003, "Ergo Office Chair", "Furniture", "Chairs", 229.00),
        (1004, "Standing Desk", "Furniture", "Tables", 399.00),
        (1005, "USB-C Hub", "Electronics", "Accessories", 49.00),
        (1006, "Desk Lamp Pro", "Furniture", "Lighting", 59.00),
        (1007, "Notebook Pack", "Office", "Paper", 12.00),
        (1008, "Wireless Mouse", "Electronics", "Accessories", 29.00),
    ],
    "product_id INT, product_name STRING, category STRING, subcategory STRING, unit_price DOUBLE",
)

stores = spark.createDataFrame(
    [
        (1, "NovaMart Austin", "Austin", "TX", "South"),
        (2, "NovaMart Dallas", "Dallas", "TX", "South"),
        (3, "NovaMart Seattle", "Seattle", "WA", "West"),
        (4, "NovaMart Chicago", "Chicago", "IL", "Central"),
        (5, "NovaMart Online", "Virtual", "NA", "Digital"),
    ],
    "store_id INT, store_name STRING, city STRING, state STRING, region STRING",
)

# Intentional messy raw orders (strings, bad email case, one bad amount later cleaned in Silver)
orders = spark.createDataFrame(
    [
        (5001, "2024-01-05", 101, 1001, 1, 1, "899.00", "credit_card"),
        (5002, "2024-01-05", 102, 1005, 2, 2, "98.00", "credit_card"),
        (5003, "2024-01-06", 103, 1002, 3, 1, "149.00", "paypal"),
        (5004, "2024-01-07", 104, 1003, 4, 1, "229.00", "credit_card"),
        (5005, "2024-01-08", 105, 1008, 1, 3, "87.00", "cash"),
        (5006, "2024-02-01", 106, 1004, 5, 1, "399.00", "credit_card"),
        (5007, "2024-02-02", 107, 1006, 2, 2, "118.00", "paypal"),
        (5008, "2024-02-03", 108, 1007, 3, 5, "60.00", "credit_card"),
        (5009, "2024-02-03", 101, 1002, 5, 1, "149.00", "credit_card"),
        (5010, "2024-02-10", 102, 1001, 5, 1, "899.00", "credit_card"),
        (5011, "2024-03-01", 103, 1005, 3, 4, "196.00", "paypal"),
        (5012, "2024-03-02", 104, 1003, 4, 2, "458.00", "credit_card"),
        (5013, "2024-03-05", 105, 1004, 1, 1, "399.00", "credit_card"),
        (5014, "2024-03-08", 106, 1008, 5, 2, "58.00", "paypal"),
        (5015, "2024-03-10", 107, 1002, 2, 1, "149.00", "cash"),
        # duplicate order_id for dedupe lesson in Silver
        (5015, "2024-03-10", 107, 1002, 2, 1, "149.00", "cash"),
        # bad amount for quality lesson
        (5016, "2024-03-12", 108, 1007, 3, 1, "-5.00", "credit_card"),
        (5017, "2024-03-15", 101, 1006, 5, 1, "59.00", "credit_card"),
        (5018, "2024-03-18", 102, 1003, 5, 1, "229.00", "paypal"),
        (5019, "2024-03-20", 103, 1001, 3, 1, "899.00", "credit_card"),
        (5020, "2024-03-22", 104, 1005, 4, 3, "147.00", "credit_card"),
    ],
    "order_id INT, order_date STRING, customer_id INT, product_id INT, store_id INT, quantity INT, amount STRING, payment_method STRING",
)

print("Customers:", customers.count(), "Products:", products.count(), "Stores:", stores.count(), "Order rows:", orders.count())

# COMMAND ----------

customers.write.mode("overwrite").option("header", True).csv(f"{LANDING_PATH}/customers")
products.write.mode("overwrite").option("header", True).csv(f"{LANDING_PATH}/products")
stores.write.mode("overwrite").option("header", True).csv(f"{LANDING_PATH}/stores")
orders.write.mode("overwrite").option("header", True).json(f"{LANDING_PATH}/orders")

# Teaching metadata table
spark.createDataFrame(
    [(SCHEMA_NAME, LANDING_PATH, dt.datetime.utcnow().isoformat())],
    "schema_name STRING, landing_path STRING, created_at STRING",
).write.mode("overwrite").saveAsTable(f"{SCHEMA_NAME}.project_config")

print("Landing files written.")
display(dbutils.fs.ls(LANDING_PATH))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Teaching checkpoint
# MAGIC Ask students:
# MAGIC - Why write files to landing **before** creating Bronze tables?
# MAGIC - Why are order amounts stored as **strings** in the raw feed?
