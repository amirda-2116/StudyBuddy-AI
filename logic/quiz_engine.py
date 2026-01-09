# logic/quiz_engine.py

import json
from logic.llm_engine import generate_response


def generate_quiz(context: str, topic: str, num_questions: int = 5):
    prompt = f"""
You are an exam quiz generator.

Generate a timed quiz for the topic "{topic}".

STRICT RULES:
- Use ONLY the content below
- Generate exactly {num_questions} questions
- Each question must have 4 options (A, B, C, D)
- Indicate the correct answer
- RETURN ONLY VALID JSON
- DO NOT include explanations
- DO NOT include markdown
- DO NOT include extra text

JSON FORMAT (MUST FOLLOW EXACTLY):

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "answer": "A"
  }}
]

CONTENT:
{context}
"""

    raw = generate_response(prompt)

    if not raw or not raw.strip():
        return []

    # ---------- CLEAN ----------
    cleaned = raw.strip()
    cleaned = cleaned.replace("```json", "")
    cleaned = cleaned.replace("```", "")

    # ---------- PARSE SAFELY ----------
    try:
        data = json.loads(cleaned)

        # Validate structure
        valid = []
        for q in data:
            if (
                isinstance(q, dict)
                and "question" in q
                and "options" in q
                and "answer" in q
                and q["answer"] in q["options"]
            ):
                valid.append(q)

        return valid

    except json.JSONDecodeError:
        # Never crash the app
        return []

