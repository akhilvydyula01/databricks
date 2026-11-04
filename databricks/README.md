# Databricks Gen AI Workspace

Databricks notebooks and Asset Bundle for the open-source Gen AI learning path.

- **Workspace:** https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022
- **GitHub repo:** https://github.com/akhilvydyula01/databricks

## Layout

```
databricks/
├── databricks.yml          # Databricks Asset Bundle
├── notebooks/gen_ai/
│   ├── basic/
│   ├── intermediate/
│   └── advanced/
└── README.md
```

## Option A — Git folder in the workspace (fastest)

1. In Databricks: **Workspace → Repos / Git folders → Add Repo**
2. URL: `https://github.com/akhilvydyula01/databricks`
3. Open notebooks under `databricks/notebooks/gen_ai/...`
4. Attach a cluster (ML runtime recommended; GPU optional)

## Option B — Databricks Asset Bundle

```bash
pip install databricks-cli
databricks auth login --host https://dbc-37e2a2e8-2739.cloud.databricks.com
cd databricks
databricks bundle validate
databricks bundle deploy -t dev
databricks bundle run genai_basic_hello -t dev
```

## Cluster tips

- Start with **Databricks Runtime ML** (includes PyTorch / Transformers friendly stack).
- First notebook cell installs any missing packages with `%pip`.
- Prefer small models (`flan-t5-small` / `flan-t5-base`) on CPU clusters.
- For LoRA fine-tuning, use a GPU node type.

## Learning order

1. `notebooks/gen_ai/basic/`
2. `notebooks/gen_ai/intermediate/`
3. `notebooks/gen_ai/advanced/`
