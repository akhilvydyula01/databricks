# Databricks notebook source
# MAGIC %md
# MAGIC # Intermediate — FAISS RAG
# MAGIC Chunk → embed → FAISS index → retrieve → generate.

# COMMAND ----------

# MAGIC %pip install -q transformers accelerate sentencepiece sentence-transformers faiss-cpu
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"
CHUNK_SIZE = 120

KNOWLEDGE = """
Generative AI creates text, images, audio, and code from prompts.
Retrieval-Augmented Generation (RAG) retrieves relevant documents before answering.
FAISS is an open-source library from Meta for fast similarity search over embeddings.
Databricks Unity Catalog centralizes data governance for tables, models, and volumes.
Vector indexes store dense embeddings so you can find semantically similar chunks.
Hallucinations happen when a model invents facts; grounding with retrieved context reduces them.
LangChain and LlamaIndex are popular open-source frameworks for LLM app orchestration.
Sentence Transformers produce embeddings useful for search, clustering, and RAG.
"""

# COMMAND ----------

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size) if words[i:i + chunk_size]]


chunks = chunk_text(KNOWLEDGE)
print(f"Chunks: {len(chunks)}")

embedder = SentenceTransformer(EMBED_MODEL)
vectors = embedder.encode(chunks, normalize_embeddings=True)
vectors = np.asarray(vectors, dtype="float32")
index = faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)
print(f"FAISS vectors: {index.ntotal}")

llm = pipeline("text2text-generation", model=LLM_MODEL, max_new_tokens=128)

# COMMAND ----------

def retrieve(query: str, k: int = 2):
    q = embedder.encode([query], normalize_embeddings=True).astype("float32")
    scores, ids = index.search(q, min(k, len(chunks)))
    return [(chunks[i], float(scores[0][rank])) for rank, i in enumerate(ids[0]) if i >= 0]


def answer(question: str, contexts):
    context = "\n".join(f"- {c}" for c in contexts)
    prompt = (
        "Use only the context to answer. If missing, say you do not know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


for question in [
    "What is FAISS used for?",
    "How does RAG reduce hallucinations?",
    "What does Unity Catalog do?",
]:
    hits = retrieve(question, k=2)
    reply = answer(question, [text for text, _ in hits])
    print("---")
    print(f"Q: {question}")
    for text, score in hits:
        print(f"  [{score:.3f}] {text[:90]}...")
    print(f"A: {reply}")
