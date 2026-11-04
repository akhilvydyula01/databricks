# Find notebooks in Databricks

Exact path after you add the GitHub repo as a Git folder:

```text
Workspace
└── Repos  (or Git folders)
    └── <your-email-or-user>
        └── databricks
            ├── projects
            │   ├── data-warehouse
            │   │   └── notebooks          ← retail DWH (00–09)
            │   └── gen-ai
            │       ├── basic / intermediate / advanced   ← local scripts
            │       └── notebooks                         ← Gen AI notebooks
            └── learning-resources
                ├── student-guide
                ├── assignments
                ├── guides
                └── youtube
```

## Setup (one time)

1. Open your workspace: https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022
2. Left sidebar → **Workspace**
3. Open **Repos** (or **Git folders**)
4. Open your user folder
5. **Add Repo** / **Create Git folder**
6. URL: `https://github.com/akhilvydyula01/databricks`
7. Create / Clone

## If the repo already exists

1. Open the `databricks` Git folder
2. **⋯ → Pull**
3. Confirm you see top-level `projects` and `learning-resources`

## First notebooks to open

- DWH: `projects/data-warehouse/notebooks/00_architecture_overview`
- Gen AI: `projects/gen-ai/notebooks/basic/01_hello_llm`

Attach a cluster → **Run all**.
