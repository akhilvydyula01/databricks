# databricks

Databricks + Gen AI learning workspace (public).

- **Workspace:** https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022
- **GitHub:** https://github.com/akhilvydyula01/databricks

## Projects

| Path | Description |
|------|-------------|
| [`gen-ai/`](./gen-ai/) | Local Python Gen AI learning path |
| [`gen-ai/basic/`](./gen-ai/basic/) | Beginner scripts |
| [`gen-ai/intermediate/`](./gen-ai/intermediate/) | Intermediate scripts |
| [`gen-ai/advanced/`](./gen-ai/advanced/) | Advanced scripts |
| [`databricks/`](./databricks/) | Databricks notebooks + Asset Bundle |

## Local quick start

```bash
cd gen-ai/basic
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python 01_hello_llm.py
```

## Databricks quick start

1. In the workspace: **Repos / Git folders → Add Repo**
2. URL: `https://github.com/akhilvydyula01/databricks`
3. Open `databricks/notebooks/gen_ai/basic/01_hello_llm`
4. Attach an ML runtime cluster and run all

See [`databricks/README.md`](./databricks/README.md) for Asset Bundle deploy steps.
