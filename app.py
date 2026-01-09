import streamlit as st
import time

from logic.file_saver import save_file
from logic.rag_engine import build_knowledge_base, retrieve_context
from logic.summary_engine import generate_summary
from logic.question_engine import generate_important_questions
from logic.mcq_engine import generate_mcqs
from logic.mock_test_engine import generate_mock_questions, evaluate_mock_answers
from logic.quiz_engine import generate_quiz


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="Exam Prep AI", layout="centered")


# =========================================================
# STYLES
# =========================================================
st.markdown("""
<style>
.stApp { background-color: #0b0614; }
h1, h2, h3 { color: #e6ddff; }
p, span, label { color: #b9a7d8; }

.stButton > button {
    background-color: #6b4eff;
    color: #ffffff;
    border-radius: 18px;
    padding: 14px;
    font-size: 17px;
    font-weight: 700;
}

input, textarea {
    background-color: #12091f !important;
    color: #e6ddff !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE INIT
# =========================================================
def init_state():
    defaults = {
        "page": "upload",
        "files_uploaded": False,
        "kb_built": False,

        "mcqs": None,
        "submitted": False,
        "user_answers": {},

        "mock_questions": None,

        "quiz_data": None,
        "quiz_index": 0,
        "quiz_score": 0,
        "feedback": None,
        "start_time": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()


# =========================================================
# PAGE 1: UPLOAD
# =========================================================
if st.session_state.page == "upload":

    st.markdown("<h1 style='text-align:center;'>STUDYBUDDY AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Your Study Partner</p>", unsafe_allow_html=True)

    st.subheader("📒 Upload Notes")
    notes = st.file_uploader(
        "Notes (PDF / DOCX / PPTX)",
        type=["pdf", "docx", "pptx"],
        accept_multiple_files=True
    )

    if notes:
        for f in notes:
            save_file(f, "notes")
        st.session_state.files_uploaded = True
        st.success("Notes uploaded")

    st.subheader("📄 Upload Syllabus")
    syllabus = st.file_uploader("Syllabus", type=["pdf", "docx"])

    if syllabus:
        save_file(syllabus, "syllabus")
        st.session_state.files_uploaded = True
        st.success("Syllabus uploaded")

    st.subheader("📝 Upload PYQs")
    pyqs = st.file_uploader(
        "PYQ Papers",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if pyqs:
        for f in pyqs:
            save_file(f, "pyq")
        st.session_state.files_uploaded = True
        st.success("PYQs uploaded")

    st.divider()

    if st.session_state.files_uploaded and not st.session_state.kb_built:
        if st.button("🚀 Start Processing"):
            with st.spinner("Building knowledge base..."):
                build_knowledge_base()
            st.session_state.kb_built = True
            st.session_state.page = "options"
            st.rerun()


# =========================================================
# PAGE 2: OPTIONS
# =========================================================
if st.session_state.page == "options":

    st.markdown("<h2 style='text-align:center;'>Choose a Mode</h2>", unsafe_allow_html=True)

    if st.button("📘 Summary", use_container_width=True):
        st.session_state.page = "summary"
        st.rerun()

    if st.button("❓ Important Questions", use_container_width=True):
        st.session_state.page = "imp_questions"
        st.rerun()

    if st.button("✅ MCQ Test", use_container_width=True):
        st.session_state.mcqs = None
        st.session_state.submitted = False
        st.session_state.page = "mcq"
        st.rerun()

    if st.button("🧠 Mock Test", use_container_width=True):
        st.session_state.mock_questions = None
        st.session_state.page = "mock"
        st.rerun()

    if st.button("⚡ Timed Quiz", use_container_width=True):
        st.session_state.quiz_data = None
        st.session_state.page = "quiz"
        st.rerun()


# =========================================================
# PAGE: SUMMARY
# =========================================================
if st.session_state.page == "summary":

    st.title("📘 Topic-wise Summary")
    topic = st.text_input("Enter topic name")

    if topic:
        with st.spinner("Generating summary..."):
            context = retrieve_context(topic)
            summary = generate_summary(context, topic)
        st.write(summary)

    if st.button("⬅ Back"):
        st.session_state.page = "options"
        st.rerun()


# =========================================================
# PAGE: IMPORTANT QUESTIONS
# =========================================================
if st.session_state.page == "imp_questions":

    st.title("❓ Important Questions")
    topic = st.text_input("Enter topic name")

    if topic:
        with st.spinner("Generating questions..."):
            context = retrieve_context(topic)
            questions = generate_important_questions(context, topic)
        st.write(questions)

    if st.button("⬅ Back"):
        st.session_state.page = "options"
        st.rerun()


# =========================================================
# PAGE: MCQ TEST
# =========================================================
# =========================================================
# PAGE: MCQ TEST (MODIFIED)
# =========================================================
if st.session_state.page == "mcq":

    st.title("✅ MCQ Test")

    topic = st.text_input("Enter topic name")
    num_q = st.slider("Number of questions", 3, 10, 5)

    if "mcqs" not in st.session_state:
        st.session_state.mcqs = None
        st.session_state.user_answers = {}
        st.session_state.submitted = False

    if st.button("Generate MCQs") and topic:
        with st.spinner("Generating MCQs..."):
            context = retrieve_context(topic)
            st.session_state.mcqs = generate_mcqs(context, topic, num_q)
            st.session_state.user_answers = {}
            st.session_state.submitted = False

    if st.session_state.mcqs:
        for i, q in enumerate(st.session_state.mcqs):
            st.markdown(f"**Q{i+1}. {q['question']}**")

            choice = st.radio(
                "Choose one:",
                options=list(q["options"].keys()),
                format_func=lambda x: f"{x}. {q['options'][x]}",
                key=f"mcq_{i}"
            )

            st.session_state.user_answers[i] = choice

        if st.button("📊 Submit Test"):
            st.session_state.submitted = True

    # ================= RESULTS =================
    if st.session_state.submitted:
        score = 0
        total = len(st.session_state.mcqs)

        st.subheader("📊 Detailed Results")

        for i, q in enumerate(st.session_state.mcqs):
            user_ans = st.session_state.user_answers.get(i)
            correct_ans = q["answer"]

            if user_ans == correct_ans:
                score += 1
                st.success(f"Q{i+1}: Correct ✅")
            else:
                st.error(
                    f"Q{i+1}: Wrong ❌ | Correct Answer: {correct_ans}. {q['options'][correct_ans]}"
                )

        st.markdown(f"## 🏆 Final Score: **{score} / {total}**")

        if score == total:
            st.success("🎉 Excellent! Perfect score!")
        elif score >= total * 0.6:
            st.warning("👍 Good job! Revise weak areas.")
        else:
            st.error("⚠️ Needs improvement. Practice more.")

    if st.button("⬅️ Back to Options"):
        st.session_state.page = "options"
        st.session_state.mcqs = None
        st.session_state.submitted = False
        st.rerun()



# =========================================================
# PAGE: MOCK TEST
# =========================================================
if st.session_state.page == "mock":

    st.title("🧠 Mock Test")
    topic = st.text_input("Topic")
    num_q = st.slider("Questions", 3, 10, 5)

    if st.button("Generate Mock Test") and topic:
        with st.spinner("Generating..."):
            context = retrieve_context(topic)
            st.session_state.mock_questions = generate_mock_questions(context, topic, num_q)
            st.session_state.mock_context = context

    if st.session_state.mock_questions:
        st.write(st.session_state.mock_questions)
        answers = st.text_area("Write your answers", height=300)

        if st.button("Submit Mock"):
            with st.spinner("Evaluating..."):
                result = evaluate_mock_answers(
                    st.session_state.mock_context,
                    st.session_state.mock_questions,
                    answers
                )
            st.write(result)

    if st.button("⬅ Back"):
        st.session_state.page = "options"
        st.rerun()


# =========================================================
# PAGE: QUIZ
# =========================================================

if st.session_state.page == "quiz":

    st.title("⚡ Timed Quiz (15 seconds per question)")

    topic = st.text_input("Enter topic name")

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.feedback = None
        st.session_state.start_time = None

    # Generate quiz
    if topic and st.session_state.quiz_data is None:
        context = retrieve_context(topic)
        st.session_state.quiz_data = generate_quiz(context, topic)
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.feedback = None
        st.session_state.start_time = time.time()
        st.rerun()

    # Show quiz question
    if st.session_state.quiz_data:

        q = st.session_state.quiz_data[st.session_state.quiz_index]

        st.markdown(
            f"### Question {st.session_state.quiz_index + 1} / {len(st.session_state.quiz_data)}"
        )
        st.markdown(f"**{q['question']}**")

        # ⏳ TIMER
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 15 - elapsed)

        st.warning(f"⏳ Time Left: {remaining} seconds")

        if remaining == 0 and st.session_state.feedback is None:
            st.session_state.feedback = "timeout"

        choice = st.radio(
            "Choose your answer:",
            list(q["options"].keys()),
            format_func=lambda x: f"{x}. {q['options'][x]}",
            key=f"quiz_{st.session_state.quiz_index}"
        )

        if st.button("Submit Answer") and st.session_state.feedback is None:
            if choice == q["answer"]:
                st.session_state.feedback = "correct"
                st.session_state.quiz_score += 1
            else:
                st.session_state.feedback = "wrong"

        # FEEDBACK
        if st.session_state.feedback:
            if st.session_state.feedback == "correct":
                st.success("Correct ✅")
            elif st.session_state.feedback == "wrong":
                st.error(f"Wrong ❌ | Correct Answer: {q['answer']}")
            else:
                st.warning(f"⏰ Time up! Correct Answer: {q['answer']}")

            if st.button("Next Question"):
                st.session_state.feedback = None
                st.session_state.quiz_index += 1
                st.session_state.start_time = time.time()

                if st.session_state.quiz_index >= len(st.session_state.quiz_data):
                    st.session_state.page = "quiz_result"
                st.rerun()


# =========================================================
# QUIZ RESULT PAGE
# =========================================================
if st.session_state.page == "quiz_result":

    st.title("🏁 Quiz Finished")

    total = len(st.session_state.quiz_data)
    score = st.session_state.quiz_score

    st.metric("Final Score", f"{score} / {total}")

    if score == total:
        st.success("🎉 Outstanding! Perfect performance!")
    elif score >= total * 0.6:
        st.warning("👍 Good effort! Review weak topics.")
    else:
        st.error("⚠️ Needs more practice!")

    if st.button("⬅ Back to Options"):
        st.session_state.page = "options"
        st.session_state.quiz_data = None
        st.rerun()
