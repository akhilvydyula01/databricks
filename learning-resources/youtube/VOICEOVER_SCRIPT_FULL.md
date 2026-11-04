# Full YouTube Voiceover Script — NovaMart Retail Data Warehouse

**Suggested title:** Build a Complete Retail Data Warehouse in Databricks (Bronze → Silver → Gold)

**Suggested length:** 12–15 minutes (detailed), or use the shorter cut below for ~8 minutes  
**Tone:** Friendly teacher, clear, not too fast  
**On screen:** Databricks workspace + GitHub repo

Record this in **your own voice** (phone mic or headset is fine). Pause where you see `[PAUSE]`.

---

## TITLE CARD (say after intro music, 0:00)

Welcome to this hands-on Databricks project.

Today we will build a complete retail data warehouse for a fictional company called NovaMart — from raw files all the way to analytics-ready tables that students and analysts can query.

This project is open source on GitHub, and you can run every notebook inside your own Databricks workspace.

---

## SECTION 1 — What this project is (0:30)

So what exactly are we building?

We are building a **lakehouse-style data warehouse** using Databricks.

That means:

1. We store and process data using Spark on Databricks.
2. We organize data in layers called **Bronze, Silver, and Gold** — also known as the **medallion architecture**.
3. In the Gold layer, we create a **star schema** — facts and dimensions — so business questions become easy SQL.

The business domain is retail sales:
- customers
- products
- stores
- orders

By the end, you will have tables like `gold_fact_sales`, `gold_dim_customer`, and SQL that answers questions such as revenue by month, top products, and store performance.

`[PAUSE]`

---

## SECTION 2 — Why students should care (1:30)

Many tutorials jump straight into clean tables and SELECT statements.

But in real companies, data arrives messy.
Amounts come as strings.
Duplicates exist.
Bad records appear.
Customer attributes change over time.

This project teaches the full path industry teams use:

- land raw data
- clean and trust it
- model it for analytics
- track history with SCD Type 2
- protect dashboards with data quality checks
- finally answer business questions

If you are teaching students, this is a perfect classroom and YouTube series project.

---

## SECTION 3 — Repo and workspace setup (2:30)

Open the public GitHub repository:
**github.com/akhilvydyula01/databricks**

In Databricks:
1. Go to Workspace
2. Open Repos or Git folders
3. Add the GitHub repo
4. Click Pull so you get the latest files

The data warehouse notebooks are here:

`notebooks` → `data_warehouse`

You will see notebooks numbered from `00` to `09`.

`[PAUSE — show folder tree on screen]`

---

## SECTION 4 — Architecture overview (3:30)

Open notebook `00_architecture_overview`.

Here is the big picture.

**Bronze** means raw.
We keep data close to how it arrived, and we add lineage columns like ingestion time and source name.

**Silver** means trusted.
We cast data types, standardize values, remove duplicates, and quarantine bad rows.

**Gold** means analytics-ready.
We build dimensions and a fact table in a star schema.

Visualize it like this:

Source files go to Bronze.
Bronze is cleaned into Silver.
Silver is modeled into Gold.
Gold feeds SQL analytics and dashboards.

`[PAUSE]`

---

## SECTION 5 — Setup and sample data (4:30)

Open notebook `01_setup_and_sample_data` and run all.

This notebook creates a schema called `retail_dwh` and generates sample NovaMart files under FileStore landing folders.

We intentionally keep some messiness in orders — for example amounts as strings, a duplicate order, and one invalid negative amount — so students can see why Silver and quality checks matter.

Teaching question for your audience:
Why write landing files first, instead of inserting straight into final tables?

Answer: landing plus Bronze preserves an auditable raw history.

---

## SECTION 6 — Bronze ingestion (5:45)

Open notebook `02_bronze_ingestion` and run all.

We read customers, products, and stores from CSV, and orders from JSON.
Then we create:

- `bronze_customers`
- `bronze_products`
- `bronze_stores`
- `bronze_orders`

Important teaching point:
In Bronze, we do **not** fix business rules yet.
We land the data and enrich it with metadata.

Show students the schema of `bronze_orders` and point out that amount is still a string.

`[PAUSE — display bronze_orders]`

---

## SECTION 7 — Silver transforms (7:00)

Open notebook `03_silver_transform`.

Now we create trust.

For customers, we trim names, lowercase emails, and standardize state and segment.

For orders, we:
- cast types
- keep only valid quantities and amounts
- deduplicate by order id
- send bad rows into `silver_orders_rejected`

This is a key lesson:
Bad data should not silently disappear.
We quarantine it so data engineers can investigate.

`[PAUSE — show rejected table]`

---

## SECTION 8 — Gold star schema (8:30)

Open notebook `04_gold_star_schema`.

Now we build the warehouse model analysts love.

Dimensions:
- `gold_dim_date`
- `gold_dim_customer`
- `gold_dim_product`
- `gold_dim_store`

Fact:
- `gold_fact_sales`

Say this clearly:
The **grain** of our fact table is one order.
Measures include quantity and gross amount.
We use surrogate keys so dimensions can evolve safely.

On screen, sketch a star: fact in the center, dimensions around it.

`[PAUSE]`

---

## SECTION 9 — SCD Type 2 (10:00)

Open notebook `05_scd2_customers`.

Customer attributes change.
For example, Aisha moves from Austin to Houston.
If we overwrite the city, we lose history.

SCD Type 2 keeps history using:
- `valid_from`
- `valid_to`
- `is_current`

After the demo change, show both versions for customer 101 and 104.

This is one of the most interview-relevant warehouse topics you can teach.

`[PAUSE — show SCD2 SQL result]`

---

## SECTION 10 — Data quality (11:15)

Open notebook `06_data_quality`.

Before publishing Gold to dashboards, we run rules:

- fact primary key uniqueness
- positive measures
- no orphan dimension keys
- reject table captured bad records

If a rule fails, we stop.
That is how you protect business users from wrong numbers.

`[PAUSE]`

---

## SECTION 11 — Analytics payoff (12:15)

Open notebook `07_analytics_sql`.

This is the moment students feel the value.

Run:
- total revenue and average order value
- revenue by month
- top products
- store performance
- segment contribution

Ask your audience live:
Which store has the highest average order value?

Then reveal the challenge query solution.

`[PAUSE]`

---

## SECTION 12 — Pipeline and next steps (13:30)

Notebook `08` runs the pipeline end to end.
Notebook `09` is a fast runner for short videos.

In production, convert these notebooks into a Databricks Job with task dependencies — setup, bronze, silver, gold, SCD2, quality, analytics.

Students can continue with the assignment:
add a Returns source and build `gold_fact_returns`.

---

## CLOSING CTA (14:15)

If you found this useful, clone the repo, pull it into Databricks Repos, and run the notebooks in order from `00` to `07`.

Repo link again:
**github.com/akhilvydyula01/databricks**

Path:
**notebooks / data_warehouse**

Like, subscribe, and tell me in the comments whether you want Part 2 — Databricks Jobs, Returns fact table, and a SQL dashboard.

Thanks for watching, and I’ll see you in the next video.

---

## Short 8-minute cut (optional)

If you want a shorter upload, only record:
- Title + what/why
- Architecture
- Bronze + Silver highlights
- Gold + one KPI SQL
- CTA

Skip deep SCD2 code and quality internals; mention them as “covered in full playlist.”
