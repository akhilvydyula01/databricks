"""
Basic Gen AI — Simple Chatbot
Multi-turn terminal chat using an open-source instruction model.
Type 'exit' or 'quit' to stop.
"""

from transformers import pipeline

MODEL_ID = "google/flan-t5-base"
MAX_HISTORY_TURNS = 4


def build_prompt(history: list[tuple[str, str]], user_message: str) -> str:
    lines = [
        "You are a helpful Gen AI tutor. Answer clearly and briefly.",
        "",
    ]
    for user, assistant in history[-MAX_HISTORY_TURNS:]:
        lines.append(f"User: {user}")
        lines.append(f"Assistant: {assistant}")
    lines.append(f"User: {user_message}")
    lines.append("Assistant:")
    return "\n".join(lines)


def main() -> None:
    print(f"Loading chatbot model: {MODEL_ID}")
    chat = pipeline(
        "text2text-generation",
        model=MODEL_ID,
        max_new_tokens=160,
    )

    history: list[tuple[str, str]] = []
    print("Chatbot ready. Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ").strip()
        if not user_message:
            continue
        if user_message.lower() in {"exit", "quit"}:
            print("Bye!")
            break

        prompt = build_prompt(history, user_message)
        reply = chat(prompt)[0]["generated_text"].strip()
        history.append((user_message, reply))
        print(f"Bot: {reply}\n")


if __name__ == "__main__":
    main()
