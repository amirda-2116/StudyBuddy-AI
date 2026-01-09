import json
from logic.llm_engine import generate_response


def generate_mcqs(context: str, topic: str, num_questions: int = 5):
    """
    Returns MCQs as a list of dicts:
    [
      {
        "question": "...",
        "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
        "answer": "A"
      }
    ]
    """

    prompt = f"""
You are an exam-oriented academic assistant.

Using ONLY the content below, generate {num_questions} MCQs
for the topic "{topic}".

Rules:
- Each question must have exactly 4 options (A, B, C, D)
- Clearly mark the correct answer
- Do NOT add explanations
- Return ONLY valid JSON
- Do NOT add any text outside JSON

FORMAT (STRICT):

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

    # ---- Safety cleanup ----
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    try:
        mcqs = json.loads(cleaned)
        return mcqs
    except:
        # fallback so app never crashes
        return []
