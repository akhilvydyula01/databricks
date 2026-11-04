# Databricks notebook source
# MAGIC %md
# MAGIC # Advanced — Multi-Agent Pipeline
# MAGIC Researcher → Critic → Writer handoff using an open-source model.

# COMMAND ----------

# MAGIC %pip install -q transformers accelerate sentencepiece
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from dataclasses import dataclass
from transformers import pipeline

MODEL_ID = "google/flan-t5-base"
llm = pipeline("text2text-generation", model=MODEL_ID, max_new_tokens=96)

CORPUS = [
    "RAG retrieves relevant chunks before generation to reduce hallucinations.",
    "LoRA trains low-rank adapters so fine-tuning is cheaper than full updates.",
    "FAISS supports dense similarity search over embedding vectors.",
    "Multi-agent systems split work across specialized roles with handoffs.",
    "Production Gen AI needs logging, evaluation, access control, and fallbacks.",
]


@dataclass
class AgentMessage:
    role: str
    content: str

# COMMAND ----------

def researcher(question: str) -> str:
    joined = "\n".join(f"- {c}" for c in CORPUS)
    prompt = (
        "You are a researcher. Extract only facts from the corpus that help answer the question.\n"
        f"Corpus:\n{joined}\n\nQuestion: {question}\nNotes:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def critic(question: str, notes: str) -> str:
    prompt = (
        "You are a critic. Check if the notes are relevant and sufficient. "
        "Reply with PASS or FAIL and one short reason.\n"
        f"Question: {question}\nNotes: {notes}\nReview:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def writer(question: str, notes: str, review: str) -> str:
    prompt = (
        "You are a writer. Produce a clear final answer using the notes. "
        "If the critic failed the notes, say you need more evidence.\n"
        f"Question: {question}\nNotes: {notes}\nCritic: {review}\nFinal answer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def run_pipeline(question: str):
    notes = researcher(question)
    review = critic(question, notes)
    final = writer(question, notes, review)
    return [
        AgentMessage("researcher", notes),
        AgentMessage("critic", review),
        AgentMessage("writer", final),
    ]


for question in [
    "Why use RAG?",
    "How does LoRA help fine-tuning?",
    "What is needed for production Gen AI?",
]:
    print("=" * 60)
    print(f"User: {question}")
    for message in run_pipeline(question):
        print(f"[{message.role}] {message.content}")
