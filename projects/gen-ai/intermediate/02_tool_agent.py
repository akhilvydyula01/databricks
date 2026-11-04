"""
Intermediate Gen AI — Tool-using agent
The LLM chooses a tool, the tool runs in Python, then the LLM writes a final answer.
Open-source only (FLAN-T5). No paid APIs.
"""

import json
import math
import re
from datetime import datetime, timezone

from transformers import pipeline

LLM_MODEL = "google/flan-t5-base"

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


def calculator(expression: str) -> str:
    allowed = re.fullmatch(r"[0-9+\-*/().%\s]+", expression or "")
    if not allowed:
        return "error: unsupported expression"
    try:
        return str(eval(expression, {"__builtins__": {}}, {"math": math}))  # noqa: S307
    except Exception as exc:  # noqa: BLE001
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


def choose_tool(llm, user_message: str) -> tuple[str, str]:
    tool_list = "\n".join(f"- {name}: {desc}" for name, desc in TOOLS.items())
    prompt = (
        "Pick one tool for the user request. Reply as JSON only.\n"
        'Format: {"tool":"name","input":"value"}\n'
        f"Tools:\n{tool_list}\n\n"
        f"User: {user_message}\nJSON:"
    )
    raw = llm(prompt)[0]["generated_text"].strip()
    try:
        payload = json.loads(raw)
        tool = str(payload.get("tool", "none")).strip()
        tool_input = str(payload.get("input", user_message)).strip()
    except json.JSONDecodeError:
        # Fallback heuristic if the small model fails JSON
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


def final_answer(llm, user_message: str, tool: str, tool_result: str) -> str:
    prompt = (
        "Write a short helpful answer for the user.\n"
        f"User: {user_message}\n"
        f"Tool used: {tool}\n"
        f"Tool result: {tool_result or 'n/a'}\n"
        "Answer:"
    )
    return llm(prompt)[0]["generated_text"].strip()


def run_agent(llm, user_message: str) -> None:
    tool, tool_input = choose_tool(llm, user_message)
    tool_result = TOOL_IMPL[tool](tool_input)
    reply = final_answer(llm, user_message, tool, tool_result)
    print(f"\nUser : {user_message}")
    print(f"Tool : {tool}({tool_input!r}) -> {tool_result}")
    print(f"Agent: {reply}")


def main() -> None:
    print(f"Loading agent model: {LLM_MODEL}")
    llm = pipeline("text2text-generation", model=LLM_MODEL, max_new_tokens=96)

    demos = [
        "Calculate 25 * (4 + 2)",
        "What time is it in UTC?",
        "What is FAISS used for?",
        "Say hello in one short sentence.",
    ]
    for message in demos:
        run_agent(llm, message)

    print("\nInteractive mode. Type 'exit' to quit.")
    while True:
        message = input("\nYou: ").strip()
        if not message:
            continue
        if message.lower() in {"exit", "quit"}:
            break
        run_agent(llm, message)


if __name__ == "__main__":
    main()
