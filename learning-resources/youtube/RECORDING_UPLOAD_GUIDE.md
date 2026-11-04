# Record & Upload Guide (Your Voice + Databricks Screen)

I cannot clone your real voice or auto-produce a full narrated YouTube course video from this chat.  
Use this workflow to create a professional upload **in your own voice**.

## What you need

- Databricks workspace open with the Git folder pulled
- Mic (headset / phone / USB mic)
- Screen recorder: **OBS Studio** (free) or Windows **Xbox Game Bar** / CapCut screen record
- Optional editor: **CapCut** or **DaVinci Resolve**

## Step-by-step recording

### 1) Prepare workspace
1. Pull latest Git folder
2. Start a cluster
3. Pre-run notebooks `01`–`07` once so tables exist (smoother recording)
4. Keep these tabs ready:
   - `00_architecture_overview`
   - `02_bronze_ingestion`
   - `03_silver_transform`
   - `04_gold_star_schema`
   - `05_scd2_customers`
   - `07_analytics_sql`
   - GitHub repo page

### 2) Record voice + screen
1. Open `VOICEOVER_SCRIPT_FULL.md` on a second monitor (teleprompter)
2. Start OBS:
   - Display capture = Databricks
   - Mic = your voice
3. Speak naturally; pause on `[PAUSE]` markers
4. If you make a mistake, pause 2 seconds and restart the sentence (easy to cut)

### 3) Fast alternative (two-pass)
1. First record **screen only** while clicking notebooks
2. Then record **voiceover only** while watching the silent video
3. Combine in CapCut

This often sounds more confident on YouTube.

### 4) Edit checklist
- Cut long silences
- Add lower-thirds:
  - Bronze / Silver / Gold
  - Star schema
  - SCD Type 2
- End screen with:
  - Repo URL
  - `projects/data-warehouse/notebooks`
- Export **1080p 16:9**, 8–15 Mbps H.264

### 5) YouTube upload metadata

**Title**
```text
Build a Retail Data Warehouse in Databricks | Bronze Silver Gold Star Schema
```

**Description**
```text
In this video I explain and demo a complete NovaMart retail data warehouse on Databricks.

What you’ll learn:
• Medallion architecture (Bronze ? Silver ? Gold)
• Star schema (fact_sales + dimensions)
• SCD Type 2 for customer history
• Data quality gates
• Analytics SQL for revenue, products, and stores

GitHub (public):
https://github.com/akhilvydyula01/databricks

Notebook path:
projects/data-warehouse/notebooks

Student assignment:
learning-resources/assignments/STUDENT_ASSIGNMENT.md

Timestamps:
00:00 Intro
00:30 What we are building
02:30 Repo + Databricks setup
03:30 Architecture
04:30 Sample data
05:45 Bronze
07:00 Silver
08:30 Gold star schema
10:00 SCD Type 2
11:15 Data quality
12:15 Analytics SQL
13:30 Jobs + next steps
14:15 CTA
```

**Tags**
```text
databricks, data warehouse, medallion architecture, bronze silver gold, star schema, SCD2, spark, data engineering, tutorial
```

**Thumbnail text ideas**
- DATABRICKS DWH
- Bronze ? Gold
- Student Project

## Captions

Upload `captions_en.srt` (in this folder) as YouTube subtitles for better reach.
