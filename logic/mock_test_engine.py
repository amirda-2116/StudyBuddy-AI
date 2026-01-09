from logic.llm_engine import generate_response


def generate_mock_questions(context: str, topic: str, num_questions: int = 5) -> str:
    prompt = f"""
You are an exam paper setter.

Using ONLY the content below, generate a mock test for the topic "{topic}".

Rules:
- Generate {num_questions} questions
- Mix short-answer and long-answer questions
- Number the questions clearly
- Do NOT include answers

CONTENT:
{context}
"""
    return generate_response(prompt)


def evaluate_mock_answers(context: str, questions: str, answers: str) -> str:
    prompt = f"""
You are an exam evaluator.

Evaluate the student's answers using ONLY the content below.

Give:
- Question-wise feedback
- Marks out of 10
- Overall performance comment

SYLLABUS CONTENT:
{context}

QUESTIONS:
{questions}

STUDENT ANSWERS:
{answers}
"""
    return generate_response(prompt)
