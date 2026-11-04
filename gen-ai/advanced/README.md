# Advanced Gen AI

Open-source projects for fine-tuning, multi-agent workflows, and production-style RAG.

Prerequisites: finish [`../basic/`](../basic/) and [`../intermediate/`](../intermediate/).

## What you will learn

1. Fine-tune a small open model with LoRA adapters
2. Orchestrate multiple specialist agents
3. Build a production-minded RAG pipeline (chunking, metadata, logging, refusal)

## Setup

```bash
cd gen-ai/advanced
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

LoRA fine-tuning is CPU-friendly with `flan-t5-small`, but a GPU makes it much faster.

## Scripts

| File | Description |
|------|-------------|
| `01_lora_finetune.py` | Tiny LoRA fine-tune + before/after demo |
| `02_multi_agent.py` | Researcher → Critic → Writer agent pipeline |
| `03_production_rag.py` | Chunked RAG with metadata filters and audit logs |

## Tips for Databricks

- Run LoRA jobs on a GPU cluster; save adapters to a UC Volume.
- Replace the in-memory store in `03_production_rag.py` with Databricks Vector Search.
- Log prompts/responses to Delta tables for evaluation and safety review.

## Safety note

These demos are educational. Add auth, PII redaction, and rate limits before production use.
