# Student Assignment — NovaMart Retail Data Warehouse

**Course project:** Databricks Data Warehouse  
**Repo:** https://github.com/akhilvydyula01/databricks  
**Notebooks:** `projects/data-warehouse/notebooks/`

## Objectives

By the end of this assignment you will:
1. Run the medallion pipeline (Bronze ? Silver ? Gold)
2. Explain star schema grain and keys
3. Extend the warehouse with a new source and mart
4. Prove quality with tests and SQL answers

## Part A — Setup (required)

1. Add the Git folder in Databricks and **Pull** latest
2. Run notebooks `00` ? `07`
3. Screenshot / export:
   - `SHOW TABLES IN retail_dwh`
   - KPI query result from notebook `07`

**Submit:** 2 screenshots + 5–8 line reflection: *Why separate Bronze and Silver?*

## Part B — Concept checks (required)

Answer briefly (2–4 sentences each):

1. What is the grain of `gold_fact_sales`?
2. Why do we keep `silver_orders_rejected` instead of deleting bad rows?
3. What problem does SCD Type 2 solve for customer city changes?
4. Name one quality rule from notebook `06` and why it matters for BI.

## Part C — Build challenge (required)

### C1. Add a Returns source

Create sample returns data (at least 5 rows) with:
- `return_id`, `order_id`, `return_date`, `reason`, `refund_amount`

Deliverables:
1. Landing files under `/FileStore/retail_dwh/landing/returns`
2. `retail_dwh.bronze_returns`
3. `retail_dwh.silver_returns` (typed, `refund_amount > 0`)
4. `retail_dwh.gold_fact_returns` joined to existing dims where possible

### C2. Analytics question

Write SQL for:
> “What is total refund amount by product category?”

### C3. Quality rule

Add at least one new DQ check, for example:
- every `order_id` in returns exists in `gold_fact_sales`

## Part D — Stretch (optional, bonus)

1. Convert notebooks `01`–`06` into a Databricks **Job** with dependencies  
2. Create a Databricks SQL dashboard with 3 visuals:
   - Revenue by month
   - Top products
   - Store AOV
3. Upgrade `gold_dim_customer` usage so facts can point to SCD2 versions valid on `order_date`

## Rubric (100 pts)

| Area | Points |
|------|--------|
| Part A setup + reflection | 20 |
| Part B concept checks | 20 |
| Part C1 returns pipeline | 30 |
| Part C2 SQL | 15 |
| Part C3 DQ rule | 15 |
| Part D stretch | +10 bonus |

## Submission checklist

- [ ] Git folder pulled
- [ ] Tables exist in `retail_dwh`
- [ ] Returns bronze/silver/gold created
- [ ] SQL answer for refunds by category
- [ ] DQ rule evidence (`dq_results` or notebook output)
- [ ] Short write-up (concepts + what you struggled with)

## Honor note for YouTube students

Pause the video and try Part C **before** watching the solution episode.
