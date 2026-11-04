# Gen AI Learning Path

Open-source Generative AI projects organized by difficulty. Built for local Python and Databricks notebooks.

| Level | Path | Focus |
|-------|------|--------|
| Basic | [`basic/`](./basic/) | Prompting, local/open models, simple chatbot, tiny RAG |
| Intermediate | [`intermediate/`](./intermediate/) | FAISS RAG, tool agents, evaluation |
| Advanced | [`advanced/`](./advanced/) | LoRA fine-tuning, multi-agent, production RAG |

## Stack (open source)

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS](https://faiss.ai/)
- [PEFT / LoRA](https://huggingface.co/docs/peft)
- Optional: [Ollama](https://ollama.com/) for fully local LLMs

## Getting started

```bash
# Basic
cd gen-ai/basic
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python 01_hello_llm.py

# Intermediate
cd ../intermediate
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python 01_faiss_rag.py

# Advanced
cd ../advanced
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python 02_multi_agent.py
```

Databricks workspace: https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022

Databricks notebook versions live in [`../databricks/notebooks/gen_ai/`](../databricks/notebooks/gen_ai/).
