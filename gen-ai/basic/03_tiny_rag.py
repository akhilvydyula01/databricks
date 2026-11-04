"""
Basic Gen AI — Tiny RAG
1) Embed a few local documents
2) Retrieve the most similar chunks for a question
3) Ask an open-source LLM to answer using only that context
"""

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


def retrieve(query: str, docs: list[str], embedder: SentenceTransformer, k: int = 2) -> list[str]:
    doc_embeddings = embedder.encode(docs, convert_to_tensor=True)
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, doc_embeddings)[0]
    top_indices = scores.topk(k=min(k, len(docs))).indices.tolist()
    return [docs[i] for i in top_indices]


def answer_with_context(question: str, context_docs: list[str], llm) -> str:
    context = "\n".join(f"- {d}" for d in context_docs)
    prompt = (
        "Answer the question using only the context. "
        "If the answer is not in the context, say you do not know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def main() -> None:
    print(f"Loading embedder: {EMBED_MODEL}")
    embedder = SentenceTransformer(EMBED_MODEL)

    print(f"Loading LLM: {LLM_MODEL}")
    llm = pipeline("text2text-generation", model=LLM_MODEL, max_new_tokens=96)

    questions = [
        "What is RAG?",
        "Where can I find open-source models?",
        "What is Databricks used for?",
    ]

    for question in questions:
        hits = retrieve(question, DOCS, embedder, k=2)
        reply = answer_with_context(question, hits, llm)
        print("\n---")
        print(f"Q: {question}")
        print("Retrieved:")
        for h in hits:
            print(f"  • {h}")
        print(f"A: {reply}")


if __name__ == "__main__":
    main()
