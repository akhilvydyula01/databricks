# How to create the NovaMart DWH Job in Databricks

The notebook paths in `retail_dwh_pipeline_job.json` use this placeholder root:

```text
/Repos/akhilvydyula01/databricks/projects/data-warehouse/notebooks/
```

If your Git folder path is different (common), update every `notebook_path` before import.

Example real path:
```text
/Repos/<your-email>/databricks/projects/data-warehouse/notebooks/01_setup_and_sample_data
```

## Option A ? UI (best for YouTube)

1. Left sidebar ? **Workflows** ? **Jobs** ? **Create job**
2. Name: `NovaMart Retail DWH Pipeline`
3. Add tasks in order with dependencies:
   - `01_setup_and_sample_data`
   - `02_bronze_ingestion` (depends on 01)
   - `03_silver_transform` (depends on 02)
   - `04_gold_star_schema` (depends on 03)
   - `05_scd2_customers` (depends on 04)
   - `06_data_quality` (depends on 05)
   - `07_analytics_sql` (depends on 06)
4. Use one shared job cluster (single-node is fine for class demos)
5. Schedule optional (JSON defaults to 6 AM America/Chicago, **paused**)
6. **Run now** once to verify

## Option B ? Import JSON

1. Fix notebook paths in `retail_dwh_pipeline_job.json`
2. Databricks ? Workflows ? Jobs ? kebab menu / API import, or:

```bash
databricks jobs create --json-file projects/data-warehouse/jobs/retail_dwh_pipeline_job.json
```

## Teaching tip

On camera, show the **task graph** (01?07). That visual alone helps students understand orchestration.
