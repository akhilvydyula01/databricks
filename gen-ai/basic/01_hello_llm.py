"""
Basic Gen AI — Hello LLM
Generate text with a small open-source model (FLAN-T5).
No API key required. Model downloads from Hugging Face on first run.
"""

from transformers import pipeline

MODEL_ID = "google/flan-t5-small"


def main() -> None:
    print(f"Loading model: {MODEL_ID}")
    generator = pipeline(
        "text2text-generation",
        model=MODEL_ID,
        max_new_tokens=128,
    )

    prompts = [
        "Explain generative AI in one short paragraph for a beginner.",
        "List three open-source LLM projects.",
        "Translate to French: Hello, how are you?",
    ]

    for prompt in prompts:
        result = generator(prompt)[0]["generated_text"]
        print("\n---")
        print(f"Prompt : {prompt}")
        print(f"Answer : {result}")


if __name__ == "__main__":
    main()
