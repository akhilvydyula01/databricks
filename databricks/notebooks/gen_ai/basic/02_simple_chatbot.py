# Databricks notebook source
# MAGIC %md
# MAGIC # Basic — Simple Chatbot
# MAGIC Multi-turn chat demo. Use the widget to send messages (Databricks has no interactive terminal `input()`).

# COMMAND ----------

# MAGIC %pip install -q transformers accelerate sentencepiece
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from transformers import pipeline

MODEL_ID = "google/flan-t5-base"
MAX_HISTORY_TURNS = 4

dbutils.widgets.text("user_message", "What is generative AI?", "User message")
dbutils.widgets.text("reset_history", "false", "Reset history (true/false)")

print(f"Loading chatbot model: {MODEL_ID}")
chat = pipeline("text2text-generation", model=MODEL_ID, max_new_tokens=160)

# COMMAND ----------

if "chat_history" not in globals() or dbutils.widgets.get("reset_history").lower() == "true":
    chat_history = []


def build_prompt(history, user_message: str) -> str:
    lines = ["You are a helpful Gen AI tutor. Answer clearly and briefly.", ""]
    for user, assistant in history[-MAX_HISTORY_TURNS:]:
        lines.append(f"User: {user}")
        lines.append(f"Assistant: {assistant}")
    lines.append(f"User: {user_message}")
    lines.append("Assistant:")
    return "\n".join(lines)


user_message = dbutils.widgets.get("user_message").strip()
prompt = build_prompt(chat_history, user_message)
reply = chat(prompt)[0]["generated_text"].strip()
chat_history.append((user_message, reply))

print(f"You: {user_message}")
print(f"Bot: {reply}")
print(f"Turns stored: {len(chat_history)}")
