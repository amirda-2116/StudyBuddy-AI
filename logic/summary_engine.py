# logic/summary_engine.py
from logic.llm_engine import generate_response

def generate_summary(context: str, topic: str) -> str:
    prompt = f"""
You are an exam-oriented academic assistant.

Generate a concise, topic-wise summary for the topic: "{topic}"

Use ONLY the content below. If information is missing, say so.

CONTENT:
{context}
"""
    return generate_response(prompt)
