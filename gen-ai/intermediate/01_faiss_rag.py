"""
Intermediate Gen AI — FAISS RAG
Chunk documents, build a FAISS index, retrieve top-k, then generate an answer.
"""

from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-base"
INDEX_PATH = Path(__file__).parent / "faiss.index"
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


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    words = text.split()
    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size) if words[i : i + chunk_size]]


def build_index(chunks: list[str], embedder: SentenceTransformer) -> faiss.IndexFlatIP:
    vectors = embedder.encode(chunks, normalize_embeddings=True)
    vectors = np.asarray(vectors, dtype="float32")
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, str(INDEX_PATH))
    return index


def retrieve(
    query: str,
    chunks: list[str],
    index: faiss.IndexFlatIP,
    embedder: SentenceTransformer,
    k: int = 3,
) -> list[tuple[str, float]]:
    q = embedder.encode([query], normalize_embeddings=True).astype("float32")
    scores, ids = index.search(q, min(k, len(chunks)))
    return [(chunks[i], float(scores[0][rank])) for rank, i in enumerate(ids[0]) if i >= 0]


def answer(question: str, contexts: list[str], llm) -> str:
    context = "\n".join(f"- {c}" for c in contexts)
    prompt = (
        "Use only the context to answer. If missing, say you do not know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def main() -> None:
    chunks = chunk_text(KNOWLEDGE)
    print(f"Chunks: {len(chunks)}")

    print(f"Loading embedder: {EMBED_MODEL}")
    embedder = SentenceTransformer(EMBED_MODEL)
    index = build_index(chunks, embedder)
    print(f"FAISS index saved to {INDEX_PATH.name}")

    print(f"Loading LLM: {LLM_MODEL}")
    llm = pipeline("text2text-generation", model=LLM_MODEL, max_new_tokens=128)

    questions = [
        "What is FAISS used for?",
        "How does RAG reduce hallucinations?",
        "What does Unity Catalog do?",
    ]

    for question in questions:
        hits = retrieve(question, chunks, index, embedder, k=2)
        reply = answer(question, [text for text, _ in hits], llm)
        print("\n---")
        print(f"Q: {question}")
        for text, score in hits:
            print(f"  [{score:.3f}] {text[:90]}...")
        print(f"A: {reply}")


if __name__ == "__main__":
    main()
