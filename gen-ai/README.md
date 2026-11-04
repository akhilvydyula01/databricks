# Gen AI Learning Path

Open-source Generative AI projects organized by difficulty. Built for local Python and Databricks notebooks.

| Level | Path | Focus |
|-------|------|--------|
| Basic | [`basic/`](./basic/) | Prompting, local/open models, simple chatbot, tiny RAG |
| Intermediate | [`intermediate/`](./intermediate/) | Agents, tools, evaluation, vector DBs |
| Advanced | [`advanced/`](./advanced/) | Fine-tuning, production pipelines, multi-agent systems |

## Stack (open source)

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Sentence Transformers](https://www.sbert.net/)
- [LangChain](https://python.langchain.com/) (introduced in intermediate)
- Optional: [Ollama](https://ollama.com/) for fully local LLMs

## Getting started

```bash
cd gen-ai/basic
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate
pip install -r requirements.txt
python 01_hello_llm.py
```

Databricks workspace: https://dbc-37e2a2e8-2739.cloud.databricks.com/?o=7474649764679022
