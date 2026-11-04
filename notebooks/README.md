# Find these notebooks in Databricks

Exact path after you add the GitHub repo as a Git folder:

```
Workspace
└── Repos  (or Git folders)
    └── <your-email-or-user>
        └── databricks
            └── notebooks
                └── gen_ai
                    ├── basic
                    │   ├── 01_hello_llm
                    │   ├── 02_simple_chatbot
                    │   └── 03_tiny_rag
                    ├── intermediate
                    └── advanced
```

## Setup (one time)

1. Open your workspace: https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022
2. Left sidebar → **Workspace**
3. Open **Repos** (sometimes labeled **Git folders**)
4. Click your user folder
5. **Add Repo** / **Create** → **Git folder**
6. Git repository URL:
   `https://github.com/akhilvydyula01/databricks`
7. Provider: GitHub → Create / Clone

## If the repo already exists but notebooks are missing

1. Open the `databricks` Git folder
2. Click the **kebab menu (⋯)** → **Pull**
3. Confirm you see a top-level `notebooks` folder

## Run the first notebook

1. Open `notebooks/gen_ai/basic/01_hello_llm`
2. Top bar → **Connect** → attach a cluster (ML runtime recommended)
3. **Run all**

Files ending in `.py` with Databricks notebook headers open as notebooks (notebook icon), not plain scripts.
