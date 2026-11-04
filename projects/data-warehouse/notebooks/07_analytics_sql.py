# Databricks notebook source
# MAGIC %md
# MAGIC # 07 — Analytics SQL (Business Questions)
# MAGIC This is the “wow” section for students and YouTube viewers.

# COMMAND ----------

# MAGIC %md
# MAGIC ## KPI board

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*) AS orders,
# MAGIC   ROUND(SUM(gross_amount), 2) AS total_revenue,
# MAGIC   ROUND(AVG(gross_amount), 2) AS avg_order_value,
# MAGIC   SUM(quantity) AS units_sold
# MAGIC FROM retail_dwh.gold_fact_sales

# COMMAND ----------

# MAGIC %md
# MAGIC ## Revenue by month

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   d.year,
# MAGIC   d.month,
# MAGIC   d.month_name,
# MAGIC   ROUND(SUM(f.gross_amount), 2) AS revenue,
# MAGIC   COUNT(*) AS orders
# MAGIC FROM retail_dwh.gold_fact_sales f
# MAGIC JOIN retail_dwh.gold_dim_date d ON f.date_key = d.date_key
# MAGIC GROUP BY d.year, d.month, d.month_name
# MAGIC ORDER BY d.year, d.month

# COMMAND ----------

# MAGIC %md
# MAGIC ## Top products

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   p.product_name,
# MAGIC   p.category,
# MAGIC   ROUND(SUM(f.gross_amount), 2) AS revenue,
# MAGIC   SUM(f.quantity) AS units
# MAGIC FROM retail_dwh.gold_fact_sales f
# MAGIC JOIN retail_dwh.gold_dim_product p ON f.product_sk = p.product_sk
# MAGIC GROUP BY p.product_name, p.category
# MAGIC ORDER BY revenue DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Store performance

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   s.store_name,
# MAGIC   s.region,
# MAGIC   ROUND(SUM(f.gross_amount), 2) AS revenue,
# MAGIC   ROUND(AVG(f.gross_amount), 2) AS avg_order_value,
# MAGIC   COUNT(*) AS orders
# MAGIC FROM retail_dwh.gold_fact_sales f
# MAGIC JOIN retail_dwh.gold_dim_store s ON f.store_sk = s.store_sk
# MAGIC GROUP BY s.store_name, s.region
# MAGIC ORDER BY revenue DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Customer segment contribution

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   c.segment,
# MAGIC   COUNT(DISTINCT c.customer_id) AS customers,
# MAGIC   ROUND(SUM(f.gross_amount), 2) AS revenue,
# MAGIC   ROUND(SUM(f.gross_amount) * 100.0 / SUM(SUM(f.gross_amount)) OVER (), 2) AS revenue_pct
# MAGIC FROM retail_dwh.gold_fact_sales f
# MAGIC JOIN retail_dwh.gold_dim_customer c ON f.customer_sk = c.customer_sk
# MAGIC GROUP BY c.segment
# MAGIC ORDER BY revenue DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Student challenge queries
# MAGIC 1. Which store has the highest average order value?
# MAGIC 2. What % of revenue is Digital region?
# MAGIC 3. Top customer by revenue (join dim_customer)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 1 solution
# MAGIC SELECT s.store_name, ROUND(AVG(f.gross_amount), 2) AS avg_order_value
# MAGIC FROM retail_dwh.gold_fact_sales f
# MAGIC JOIN retail_dwh.gold_dim_store s ON f.store_sk = s.store_sk
# MAGIC GROUP BY s.store_name
# MAGIC ORDER BY avg_order_value DESC
# MAGIC LIMIT 1
