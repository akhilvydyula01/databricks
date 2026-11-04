# Databricks notebook source
# MAGIC %md
# MAGIC # Intermediate — Eval Prompts
# MAGIC Score generated answers with contains / token F1 / groundedness metrics.

# COMMAND ----------

# MAGIC %pip install -q transformers accelerate sentencepiece
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from dataclasses import dataclass
from transformers import pipeline

MODEL_ID = "google/flan-t5-base"
llm = pipeline("text2text-generation", model=MODEL_ID, max_new_tokens=64)


@dataclass
class Example:
    question: str
    context: str
    expected: str


EVAL_SET = [
    Example("What does RAG stand for?", "RAG means Retrieval-Augmented Generation.", "Retrieval-Augmented Generation"),
    Example("Who created FAISS?", "FAISS is an open-source library from Meta for similarity search.", "Meta"),
    Example("What color is the sky on Mars?", "FAISS stores vector embeddings for search.", "I do not know"),
]

# COMMAND ----------

def tokenize(text: str):
    return {tok for tok in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split() if tok}


def token_f1(prediction: str, expected: str) -> float:
    pred_tokens, expected_tokens = tokenize(prediction), tokenize(expected)
    if not pred_tokens or not expected_tokens:
        return 0.0
    overlap = len(pred_tokens & expected_tokens)
    precision = overlap / len(pred_tokens)
    recall = overlap / len(expected_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def groundedness(prediction: str, context: str) -> float:
    pred_tokens, context_tokens = tokenize(prediction), tokenize(context)
    if not pred_tokens:
        return 0.0
    stop = {"the", "a", "an", "is", "to", "of", "and", "for", "in", "on", "do", "not", "know", "i"}
    content = pred_tokens - stop
    if not content:
        return 1.0 if "do not know" in prediction.lower() else 0.0
    return len(content & context_tokens) / len(content)


rows = []
for example in EVAL_SET:
    prompt = (
        "Answer using only the context. If the answer is not present, say I do not know.\n"
        f"Context: {example.context}\nQuestion: {example.question}\nAnswer:"
    )
    prediction = llm(prompt)[0]["generated_text"].strip()
    metrics = {
        "contains": 1.0 if example.expected.lower() in prediction.lower() else 0.0,
        "token_f1": token_f1(prediction, example.expected),
        "groundedness": groundedness(prediction, example.context),
    }
    rows.append(metrics)
    print("---")
    print(f"Q: {example.question}")
    print(f"Expected : {example.expected}")
    print(f"Predicted: {prediction}")
    print(metrics)

print("=== Summary ===")
print(f"Avg token F1 : {sum(r['token_f1'] for r in rows) / len(rows):.2f}")
print(f"Avg grounded : {sum(r['groundedness'] for r in rows) / len(rows):.2f}")
