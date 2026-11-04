# Databricks Asset Bundle

Bundle config for deploying jobs from this repo.

- **Workspace:** https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022
- **Projects:** [`../projects/`](../projects/)
- **Learning resources:** [`../learning-resources/`](../learning-resources/)

## Layout

```text
databricks/
├── databricks.yml
└── resources/jobs.yml
```

Notebook source paths point to:

- `../projects/gen-ai/notebooks/...`
- `../projects/data-warehouse/notebooks/...`

## Deploy

```bash
pip install databricks-cli
databricks auth login --host https://dbc-37e2a2e8-2739.cloud.databricks.com
cd databricks
databricks bundle validate
databricks bundle deploy -t dev
```

## Git folder (no bundle required)

Most students should just:

1. Add Git folder → `https://github.com/akhilvydyula01/databricks`
2. Pull
3. Open notebooks under `projects/...`
