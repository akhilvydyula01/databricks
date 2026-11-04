# 20-Minute YouTube Demo Cut

Use this when you need a **fast, high-retention** explainer. Full course remains notebooks `00`–`08`.

## Title

**Build a Retail Data Warehouse in Databricks in 20 Minutes (Bronze → Gold)**

## Runtime plan

| Time | Segment | Notebook / action | On-screen goal |
|------|---------|-------------------|----------------|
| 0:00–0:45 | Hook | Architecture slide | Promise: raw files → KPI SQL |
| 0:45–3:00 | Architecture | `00` | Medallion + star in 2 minutes |
| 3:00–6:00 | Data + Bronze | `01` then `02` (Run All) | Show landing files + `bronze_orders` |
| 6:00–10:00 | Silver | `03` | Dedupe + rejected negative amount |
| 10:00–14:00 | Gold star | `04` | `gold_fact_sales` + dims |
| 14:00–16:30 | SCD2 highlight | `05` SQL only | Customer 101 Austin→Houston history |
| 16:30–18:00 | Quality | `06` summary table | PASS/FAIL board |
| 18:00–19:30 | Analytics payoff | `07` top 2 SQL cells | Revenue by month + top products |
| 19:30–20:00 | CTA | Repo link | Pull Git folder + assignment |

## Exact talking track (short)

**Hook:**  
“Most students learn SQL on clean tables. Real work starts with messy files. In 20 minutes we’ll build a retail warehouse in Databricks using Bronze, Silver, and Gold.”

**Architecture:**  
“Bronze keeps raw history. Silver makes data trusted. Gold is the star schema analysts query.”

**Bronze:**  
“Notice amounts are strings. That’s intentional. We don’t fix business rules in Bronze.”

**Silver:**  
“Here we cast types, drop invalid amounts, and dedupe order 5015. Rejected rows go to a reject table — not into the void.”

**Gold:**  
“Fact grain is one order. Dimensions describe who, what, where, and when.”

**SCD2:**  
“When Aisha moves from Austin to Houston, we keep both versions with valid_from / valid_to.”

**Quality:**  
“No unique sales_key, no dashboard. Gates protect BI.”

**CTA:**  
“Clone the public repo, Pull in Repos, run `notebooks/data_warehouse`, then try the student assignment — add a Returns fact.”

## What to skip in the 20-min cut

- Deep MERGE code walkthrough (mention only)
- Notebook `08` full pipeline runner (show Job graph screenshot instead)
- Long student Q&A (save for livestream / part 2)

## B-roll / visuals checklist

- [ ] Medallion diagram
- [ ] Star schema sketch
- [ ] `display(bronze_orders)`
- [ ] Rejected orders table
- [ ] SCD2 before/after for customer 101
- [ ] Revenue-by-month chart/table
- [ ] GitHub repo + Repos Pull

## End screen text

```text
Repo: github.com/akhilvydyula01/databricks
Path: notebooks/data_warehouse
Next: Student Assignment (Returns pipeline)
```

## Optional part-2 teaser

“Part 2: we schedule this as a Databricks Job and add Returns + a SQL dashboard.”
