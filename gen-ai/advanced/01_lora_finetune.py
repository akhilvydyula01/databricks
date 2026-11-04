"""
Advanced Gen AI — LoRA fine-tuning (tiny demo)
Fine-tune FLAN-T5-small with LoRA on a few Gen AI Q&A pairs, then compare outputs.
Designed to run on CPU for learning; use GPU on Databricks for real jobs.
"""

from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig, PeftModel, TaskType, get_peft_model
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
)

BASE_MODEL = "google/flan-t5-small"
ADAPTER_DIR = Path(__file__).parent / "lora-adapter"

TRAIN_ROWS = [
    {"question": "What is RAG?", "answer": "RAG retrieves relevant documents, then generates an answer grounded in them."},
    {"question": "What is LoRA?", "answer": "LoRA fine-tunes small adapter weights instead of updating the full model."},
    {"question": "What is FAISS?", "answer": "FAISS is Meta's open-source library for fast vector similarity search."},
    {"question": "What is a hallucination?", "answer": "A hallucination is when a model invents facts that are not supported by evidence."},
    {"question": "What is an embedding?", "answer": "An embedding is a numeric vector that represents text meaning for search and clustering."},
    {"question": "What is Unity Catalog?", "answer": "Unity Catalog is Databricks governance for data, AI assets, and access control."},
]


def preprocess(tokenizer, rows: list[dict]) -> Dataset:
    def _map(batch):
        inputs = tokenizer(
            [f"Answer briefly: {q}" for q in batch["question"]],
            truncation=True,
            padding="max_length",
            max_length=64,
        )
        labels = tokenizer(
            batch["answer"],
            truncation=True,
            padding="max_length",
            max_length=64,
        )
        inputs["labels"] = labels["input_ids"]
        return inputs

    return Dataset.from_list(rows).map(_map, batched=True, remove_columns=["question", "answer"])


def generate(model, tokenizer, question: str) -> str:
    prompt = f"Answer briefly: {question}"
    encoded = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**encoded, max_new_tokens=48)
    return tokenizer.decode(output[0], skip_special_tokens=True)


def main() -> None:
    print(f"Loading base model: {BASE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    base_model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL)

    sample_q = "What is LoRA?"
    print("\nBefore fine-tune:")
    print(f"Q: {sample_q}")
    print(f"A: {generate(base_model, tokenizer, sample_q)}")

    lora_config = LoraConfig(
        task_type=TaskType.SEQ_2_SEQ_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["q", "v"],
    )
    model = get_peft_model(base_model, lora_config)
    model.print_trainable_parameters()

    train_ds = preprocess(tokenizer, TRAIN_ROWS)
    args = TrainingArguments(
        output_dir=str(Path(__file__).parent / "outputs"),
        per_device_train_batch_size=2,
        num_train_epochs=8,
        learning_rate=1e-3,
        logging_steps=5,
        save_strategy="no",
        report_to=[],
        use_cpu=not torch.cuda.is_available(),
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
        data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model),
    )
    print("\nTraining LoRA adapters...")
    trainer.train()

    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(ADAPTER_DIR)
    tokenizer.save_pretrained(ADAPTER_DIR)
    print(f"Saved adapters to {ADAPTER_DIR}")

    tuned = PeftModel.from_pretrained(
        AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL),
        ADAPTER_DIR,
    )
    print("\nAfter fine-tune:")
    for row in TRAIN_ROWS[:3]:
        print(f"Q: {row['question']}")
        print(f"A: {generate(tuned, tokenizer, row['question'])}\n")


if __name__ == "__main__":
    main()
