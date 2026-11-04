"""
Advanced Gen AI — Multi-agent pipeline
Researcher gathers notes → Critic checks grounding → Writer produces the final answer.
"""

from dataclasses import dataclass

from transformers import pipeline

LLM_MODEL = "google/flan-t5-base"

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


def researcher(llm, question: str) -> str:
    joined = "\n".join(f"- {c}" for c in CORPUS)
    prompt = (
        "You are a researcher. Extract only facts from the corpus that help answer the question.\n"
        f"Corpus:\n{joined}\n\nQuestion: {question}\nNotes:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def critic(llm, question: str, notes: str) -> str:
    prompt = (
        "You are a critic. Check if the notes are relevant and sufficient. "
        "Reply with PASS or FAIL and one short reason.\n"
        f"Question: {question}\nNotes: {notes}\nReview:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def writer(llm, question: str, notes: str, review: str) -> str:
    prompt = (
        "You are a writer. Produce a clear final answer using the notes. "
        "If the critic failed the notes, say you need more evidence.\n"
        f"Question: {question}\nNotes: {notes}\nCritic: {review}\nFinal answer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def run_pipeline(llm, question: str) -> list[AgentMessage]:
    notes = researcher(llm, question)
    review = critic(llm, question, notes)
    final = writer(llm, question, notes, review)
    return [
        AgentMessage("researcher", notes),
        AgentMessage("critic", review),
        AgentMessage("writer", final),
    ]


def main() -> None:
    print(f"Loading multi-agent model: {LLM_MODEL}")
    llm = pipeline("text2text-generation", model=LLM_MODEL, max_new_tokens=96)

    questions = [
        "Why use RAG?",
        "How does LoRA help fine-tuning?",
        "What is needed for production Gen AI?",
    ]

    for question in questions:
        print("\n" + "=" * 60)
        print(f"User: {question}")
        for message in run_pipeline(llm, question):
            print(f"[{message.role}] {message.content}")


if __name__ == "__main__":
    main()
