# Basic Gen AI

Beginner projects using open-source models. No paid API keys required for the core scripts (Hugging Face downloads models on first run).

## What you will learn

1. Run a small open-source LLM for text generation
2. Build a simple multi-turn chatbot
3. Build a tiny RAG (retrieve ? answer) pipeline

## Setup

```bash
cd projects/gen-ai/basic
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

First run may download model weights (a few hundred MB to a few GB depending on the model).

## Scripts

| File | Description |
|------|-------------|
| `01_hello_llm.py` | Generate text with a small open model |
| `02_simple_chatbot.py` | Terminal chatbot with conversation history |
| `03_tiny_rag.py` | Embed docs ? retrieve ? answer with an LLM |

## Tips for Databricks

- Attach a cluster with Python 3.10+ and install the same packages from `requirements.txt`.
- For GPU acceleration on Databricks, prefer a GPU runtime and keep the model id small (`google/flan-t5-small` or similar).
- Upload this folder as a Databricks Repo synced to GitHub: `akhilvydyula01/databricks`.

## Next

When these scripts feel comfortable, move to [`../intermediate/`](../intermediate/).
