# Databricks notebook source
# MAGIC %md
# MAGIC # Basic — Tiny RAG
# MAGIC Embed docs → retrieve → answer with an open-source LLM.

# COMMAND ----------

# MAGIC %pip install -q transformers accelerate sentencepiece sentence-transformers
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-small"

DOCS = [
    "Generative AI creates new content such as text, images, or code from prompts.",
    "Hugging Face hosts open-source models like FLAN-T5, BERT, and Llama variants.",
    "RAG means Retrieval-Augmented Generation: retrieve relevant docs, then generate an answer.",
    "Databricks is a lakehouse platform used for data engineering, analytics, and ML.",
    "Open-source Gen AI lets you run models locally or on your own cloud without paid APIs.",
]

print(f"Loading embedder: {EMBED_MODEL}")
embedder = SentenceTransformer(EMBED_MODEL)
print(f"Loading LLM: {LLM_MODEL}")
llm = pipeline("text2text-generation", model=LLM_MODEL, max_new_tokens=96)

# COMMAND ----------

def retrieve(query: str, docs, embedder, k: int = 2):
    doc_embeddings = embedder.encode(docs, convert_to_tensor=True)
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, doc_embeddings)[0]
    top_indices = scores.topk(k=min(k, len(docs))).indices.tolist()
    return [docs[i] for i in top_indices]


def answer_with_context(question: str, context_docs, llm) -> str:
    context = "\n".join(f"- {d}" for d in context_docs)
    prompt = (
        "Answer the question using only the context. "
        "If the answer is not in the context, say you do not know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


questions = [
    "What is RAG?",
    "Where can I find open-source models?",
    "What is Databricks used for?",
]

for question in questions:
    hits = retrieve(question, DOCS, embedder, k=2)
    reply = answer_with_context(question, hits, llm)
    print("---")
    print(f"Q: {question}")
    for h in hits:
        print(f"  • {h}")
    print(f"A: {reply}")
