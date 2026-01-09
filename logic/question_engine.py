from logic.llm_engine import generate_response

def generate_important_questions(context: str, topic: str) -> str:
    prompt = f"""
You are an exam-oriented academic assistant.

Based ONLY on the content below, generate important exam questions
for the topic "{topic}" along with clear, concise answers.

Guidelines:
- Include both short-answer and long-answer questions
- Number the questions
- Write answers directly below each question
- Do NOT add information outside the given content

CONTENT:
{context}
"""
    return generate_response(prompt)
