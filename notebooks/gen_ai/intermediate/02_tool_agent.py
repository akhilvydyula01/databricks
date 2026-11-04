# Databricks notebook source
# MAGIC %md
# MAGIC # Intermediate — Tool Agent
# MAGIC LLM chooses a tool → tool runs in Python → LLM writes the final answer.

# COMMAND ----------

# MAGIC %pip install -q transformers accelerate sentencepiece
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import json
import math
import re
from datetime import datetime, timezone
from transformers import pipeline

MODEL_ID = "google/flan-t5-base"
llm = pipeline("text2text-generation", model=MODEL_ID, max_new_tokens=96)

TOOLS = {
    "calculator": "Evaluate a math expression like 12 * (3 + 4).",
    "utc_time": "Return the current UTC date and time.",
    "kb_search": "Search a tiny local knowledge base for Gen AI facts.",
    "none": "Answer directly without a tool.",
}

KB = [
    "FAISS is used for fast vector similarity search.",
    "RAG retrieves documents before generation to ground answers.",
    "LoRA fine-tunes a small set of adapter weights instead of the full model.",
]

# COMMAND ----------

def calculator(expression: str) -> str:
    allowed = re.fullmatch(r"[0-9+\-*/().%\s]+", expression or "")
    if not allowed:
        return "error: unsupported expression"
    try:
        return str(eval(expression, {"__builtins__": {}}, {"math": math}))
    except Exception as exc:
        return f"error: {exc}"


def utc_time(_: str = "") -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def kb_search(query: str) -> str:
    q = (query or "").lower()
    hits = [item for item in KB if any(token in item.lower() for token in q.split())]
    return " | ".join(hits[:3]) if hits else "no local results"


TOOL_IMPL = {
    "calculator": calculator,
    "utc_time": utc_time,
    "kb_search": kb_search,
    "none": lambda _: "",
}


def choose_tool(user_message: str):
    tool_list = "\n".join(f"- {name}: {desc}" for name, desc in TOOLS.items())
    prompt = (
        "Pick one tool for the user request. Reply as JSON only.\n"
        'Format: {"tool":"name","input":"value"}\n'
        f"Tools:\n{tool_list}\n\nUser: {user_message}\nJSON:"
    )
    raw = llm(prompt)[0]["generated_text"].strip()
    try:
        payload = json.loads(raw)
        tool = str(payload.get("tool", "none")).strip()
        tool_input = str(payload.get("input", user_message)).strip()
    except json.JSONDecodeError:
        lower = user_message.lower()
        if any(op in user_message for op in "+-*/") or "calculate" in lower:
            tool, tool_input = "calculator", user_message
        elif "time" in lower or "date" in lower:
            tool, tool_input = "utc_time", ""
        elif any(word in lower for word in ("faiss", "rag", "lora", "vector")):
            tool, tool_input = "kb_search", user_message
        else:
            tool, tool_input = "none", ""
    if tool not in TOOL_IMPL:
        tool = "none"
    return tool, tool_input


def final_answer(user_message: str, tool: str, tool_result: str) -> str:
    prompt = (
        "Write a short helpful answer for the user.\n"
        f"User: {user_message}\nTool used: {tool}\nTool result: {tool_result or 'n/a'}\nAnswer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def run_agent(user_message: str):
    tool, tool_input = choose_tool(user_message)
    tool_result = TOOL_IMPL[tool](tool_input)
    reply = final_answer(user_message, tool, tool_result)
    print(f"User : {user_message}")
    print(f"Tool : {tool}({tool_input!r}) -> {tool_result}")
    print(f"Agent: {reply}")
    print("---")


for message in [
    "Calculate 25 * (4 + 2)",
    "What time is it in UTC?",
    "What is FAISS used for?",
    "Say hello in one short sentence.",
]:
    run_agent(message)
