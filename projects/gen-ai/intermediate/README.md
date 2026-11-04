# Intermediate Gen AI

Open-source projects that go beyond toy demos: real vector search, tool-using agents, and simple evaluation.

Prerequisites: finish [`../basic/`](../basic/) first.

## What you will learn

1. Build RAG with a FAISS vector index (chunk ? embed ? search ? generate)
2. Route questions to tools (calculator, search, weather stub) then answer
3. Score answers with lightweight automatic evaluation metrics

## Setup

```bash
cd projects/gen-ai/intermediate
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Scripts

| File | Description |
|------|-------------|
| `01_faiss_rag.py` | Persistent FAISS index + RAG over a knowledge base |
| `02_tool_agent.py` | Agent that picks tools, runs them, then replies |
| `03_eval_prompts.py` | Evaluate generated answers vs expected answers |

## Tips for Databricks

- Install packages on the cluster from `requirements.txt`.
- Store FAISS indexes / embeddings on DBFS or Unity Catalog volumes for reuse.
- Swap `google/flan-t5-base` for a larger open model when you have GPU.

## Next

Continue to [`../advanced/`](../advanced/) for fine-tuning, multi-agent systems, and production RAG patterns.
