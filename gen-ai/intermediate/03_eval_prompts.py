"""
Intermediate Gen AI — Lightweight evaluation
Generate answers, then score them with exact/token overlap and a simple groundedness check.
"""

from dataclasses import dataclass

from transformers import pipeline

LLM_MODEL = "google/flan-t5-base"


@dataclass
class Example:
    question: str
    context: str
    expected: str


EVAL_SET = [
    Example(
        question="What does RAG stand for?",
        context="RAG means Retrieval-Augmented Generation.",
        expected="Retrieval-Augmented Generation",
    ),
    Example(
        question="Who created FAISS?",
        context="FAISS is an open-source library from Meta for similarity search.",
        expected="Meta",
    ),
    Example(
        question="What color is the sky on Mars?",
        context="FAISS stores vector embeddings for search.",
        expected="I do not know",
    ),
]


def tokenize(text: str) -> set[str]:
    return {tok for tok in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split() if tok}


def token_f1(prediction: str, expected: str) -> float:
    pred_tokens = tokenize(prediction)
    expected_tokens = tokenize(expected)
    if not pred_tokens or not expected_tokens:
        return 0.0
    overlap = len(pred_tokens & expected_tokens)
    precision = overlap / len(pred_tokens)
    recall = overlap / len(expected_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def contains_expected(prediction: str, expected: str) -> float:
    return 1.0 if expected.lower() in prediction.lower() else 0.0


def groundedness(prediction: str, context: str) -> float:
    """Share of prediction tokens that appear in the context (rough grounding proxy)."""
    pred_tokens = tokenize(prediction)
    context_tokens = tokenize(context)
    if not pred_tokens:
        return 0.0
    # Common stopwords inflate scores; ignore a tiny set.
    stop = {"the", "a", "an", "is", "to", "of", "and", "for", "in", "on", "do", "not", "know", "i"}
    content = pred_tokens - stop
    if not content:
        return 1.0 if "do not know" in prediction.lower() else 0.0
    return len(content & context_tokens) / len(content)


def generate_answer(llm, example: Example) -> str:
    prompt = (
        "Answer using only the context. If the answer is not present, say I do not know.\n"
        f"Context: {example.context}\n"
        f"Question: {example.question}\n"
        "Answer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def main() -> None:
    print(f"Loading model: {LLM_MODEL}")
    llm = pipeline("text2text-generation", model=LLM_MODEL, max_new_tokens=64)

    rows = []
    for example in EVAL_SET:
        prediction = generate_answer(llm, example)
        metrics = {
            "contains": contains_expected(prediction, example.expected),
            "token_f1": token_f1(prediction, example.expected),
            "groundedness": groundedness(prediction, example.context),
        }
        rows.append((example, prediction, metrics))
        print("\n---")
        print(f"Q: {example.question}")
        print(f"Expected : {example.expected}")
        print(f"Predicted: {prediction}")
        print(
            "Metrics  : "
            f"contains={metrics['contains']:.2f} "
            f"token_f1={metrics['token_f1']:.2f} "
            f"groundedness={metrics['groundedness']:.2f}"
        )

    avg_f1 = sum(m["token_f1"] for _, _, m in rows) / len(rows)
    avg_ground = sum(m["groundedness"] for _, _, m in rows) / len(rows)
    print("\n=== Summary ===")
    print(f"Examples     : {len(rows)}")
    print(f"Avg token F1 : {avg_f1:.2f}")
    print(f"Avg grounded : {avg_ground:.2f}")


if __name__ == "__main__":
    main()
