# Databricks notebook source
# MAGIC %md
# MAGIC # Advanced — Production-minded RAG
# MAGIC Metadata filters, confidence gating, refusal, and audit logging to DBFS.

# COMMAND ----------

# MAGIC %pip install -q transformers accelerate sentencepiece sentence-transformers faiss-cpu
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"
LOG_PATH = Path("/tmp/rag_audit.jsonl")
MIN_SCORE = 0.25


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source: str
    product: str


@dataclass
class RagResult:
    question: str
    answer: str
    sources: list[str]
    top_score: float
    refused: bool
    timestamp: str


DOCS = [
    Chunk("c1", "RAG retrieves relevant documents before answering to ground the model.", "wiki/rag.md", "genai"),
    Chunk("c2", "FAISS is used for fast similarity search over dense vectors.", "wiki/faiss.md", "search"),
    Chunk("c3", "LoRA fine-tunes adapter weights and keeps the base model mostly frozen.", "wiki/lora.md", "training"),
    Chunk("c4", "Databricks Vector Search stores embeddings and supports ANN queries.", "wiki/databricks.md", "databricks"),
    Chunk("c5", "Audit logs should capture prompt, retrieved sources, scores, and final answer.", "wiki/ops.md", "ops"),
]

# COMMAND ----------

embedder = SentenceTransformer(EMBED_MODEL)
llm = pipeline("text2text-generation", model=LLM_MODEL, max_new_tokens=96)
vectors = embedder.encode([c.text for c in DOCS], normalize_embeddings=True)
vectors = np.asarray(vectors, dtype="float32")
index = faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)


def retrieve(question: str, product_filter: str | None = None, k: int = 2):
    query = embedder.encode([question], normalize_embeddings=True).astype("float32")
    scores, ids = index.search(query, len(DOCS))
    hits = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0:
            continue
        chunk = DOCS[idx]
        if product_filter and chunk.product != product_filter:
            continue
        hits.append((chunk, float(score)))
        if len(hits) >= k:
            break
    return hits


def generate_answer(question: str, hits) -> RagResult:
    timestamp = datetime.now(timezone.utc).isoformat()
    top_score = hits[0][1] if hits else 0.0
    if not hits or top_score < MIN_SCORE:
        return RagResult(
            question=question,
            answer="I do not have enough grounded evidence to answer that.",
            sources=[],
            top_score=top_score,
            refused=True,
            timestamp=timestamp,
        )

    context = "\n".join(f"[{c.source}] {c.text}" for c, _ in hits)
    prompt = (
        "Answer using only the sources. Cite source filenames in brackets. "
        "If unsupported, refuse.\n"
        f"Sources:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    answer = llm(prompt)[0]["generated_text"].strip()
    return RagResult(
        question=question,
        answer=answer,
        sources=[c.source for c, _ in hits],
        top_score=top_score,
        refused=False,
        timestamp=timestamp,
    )


def write_audit(result: RagResult) -> None:
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(result)) + "\n")

# COMMAND ----------

for question, product in [
    ("How does RAG help?", None),
    ("What is LoRA?", "training"),
    ("Who won the 1800 chess world cup on Mars?", None),
]:
    hits = retrieve(question, product_filter=product, k=2)
    result = generate_answer(question, hits)
    write_audit(result)
    print("---")
    print(f"Q: {question}")
    print(f"Filter: {product or 'none'} | score={result.top_score:.3f} | refused={result.refused}")
    print(f"Sources: {result.sources}")
    print(f"A: {result.answer}")

print(f"Audit log: {LOG_PATH}")
display(spark.read.json(str(LOG_PATH)))
