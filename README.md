# databricks

Public teaching workspace for **Gen AI** and a full **Retail Data Warehouse** on Databricks.

- **Workspace:** https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022
- **GitHub:** https://github.com/akhilvydyula01/databricks

## Projects

| Path | Description |
|------|-------------|
| [`data-warehouse/`](./data-warehouse/) | Retail DWH teaching project + YouTube guide |
| [`notebooks/data_warehouse/`](./notebooks/data_warehouse/) | DWH Databricks notebooks (00→08) |
| [`gen-ai/`](./gen-ai/) | Local Python Gen AI learning path |
| [`notebooks/gen_ai/`](./notebooks/gen_ai/) | Gen AI Databricks notebooks |
| [`databricks/`](./databricks/) | Asset Bundle config |

## Student PDF (print / share in class)

**[docs/student-guide/Databricks_Student_Project_Guide.pdf](./docs/student-guide/Databricks_Student_Project_Guide.pdf)**  
Includes architecture images for medallion, star schema, SCD2, and the full project map.

## YouTube / classroom: Data Warehouse

1. Workspace → **Repos** → Add Git folder → `https://github.com/akhilvydyula01/databricks`
2. **Pull** latest
3. Open **`notebooks/data_warehouse/00_architecture_overview`**
4. Attach a cluster → run notebooks **00 → 08**

- Full script: [`data-warehouse/YOUTUBE_TEACHING_GUIDE.md`](./data-warehouse/YOUTUBE_TEACHING_GUIDE.md)
- 20-min demo: [`data-warehouse/YOUTUBE_20MIN_DEMO.md`](./data-warehouse/YOUTUBE_20MIN_DEMO.md)
- Student assignment: [`data-warehouse/STUDENT_ASSIGNMENT.md`](./data-warehouse/STUDENT_ASSIGNMENT.md)
- Job JSON: [`data-warehouse/jobs/`](./data-warehouse/jobs/)

## Gen AI quick start

```bash
cd gen-ai/basic
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python 01_hello_llm.py
```
