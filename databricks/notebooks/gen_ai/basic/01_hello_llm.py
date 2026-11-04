# Databricks notebook source
# MAGIC %md
# MAGIC # Basic — Hello LLM
# MAGIC Generate text with open-source FLAN-T5. No paid API key required.

# COMMAND ----------

# MAGIC %pip install -q transformers accelerate sentencepiece
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from transformers import pipeline

MODEL_ID = "google/flan-t5-small"
print(f"Loading model: {MODEL_ID}")
generator = pipeline("text2text-generation", model=MODEL_ID, max_new_tokens=128)

# COMMAND ----------

prompts = [
    "Explain generative AI in one short paragraph for a beginner.",
    "List three open-source LLM projects.",
    "Translate to French: Hello, how are you?",
]

for prompt in prompts:
    result = generator(prompt)[0]["generated_text"]
    print("---")
    print(f"Prompt : {prompt}")
    print(f"Answer : {result}")
