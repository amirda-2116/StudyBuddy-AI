import streamlit as st
from logic.file_saver import save_file
from logic.rag_engine import build_knowledge_base
from logic.mock_test_engine import generate_mock_questions, evaluate_mock_answers
from logic.quiz_engine import generate_quiz
import time


st.set_page_config(page_title="Exam Prep AI")
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #0b0614;
}

/* Headings */
h1, h2, h3 {
    color: #e6ddff;
}

/* Normal text */
p, span, label {
    color: #b9a7d8;
}

/* Cards */
.card {
    background-color: #1a1026;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    color: #e6ddff;
    font-size: 18px;
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    background-color: #6b4eff;
    color: #f5f3ff;          /* brighter lavender-white */
    border-radius: 18px;
    padding: 16px;           /* slightly bigger */
    font-size: 18px;         /* more readable */
    font-weight: 800;        /* bolder text */
    letter-spacing: 0.5px;   /* cleaner look */
}


.stButton > button:hover {
    background-color: #8a6cff;
    color: #ffffff;
}


/* Input fields */
input, textarea {
    background-color: #12091f !important;
    color: #e6ddff !important;
    border-radius: 12px !important;
    border: 1px solid #3a275f !important;
}

/* Radio buttons */
.stRadio > div {
    color: #e6ddff;
}

/* SUCCESS (Correct Answer) */
.stSuccess {
    background-color: #1f3d2b !important;
    color: #b6f2c2 !important;
    border-radius: 12px;
    font-weight: 600;
}

/* ERROR (Wrong Answer) */
.stError {
    background-color: #3d1f28 !important;
    color: #f4b6b6 !important;
    border-radius: 12px;
    font-weight: 600;
}

/* Warning */
.stWarning {
    background-color: #2b1f3d !important;
    color: #e6ddff !important;
    border-radius: 12px;
}

/* Info boxes */
.stInfo {
    background-color: #23163a !important;
    color: #e6ddff !important;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SESSION STATE
# -------------------------
if "kb_built" not in st.session_state:
    st.session_state.kb_built = False

if "files_uploaded" not in st.session_state:
    st.session_state.files_uploaded = False

if "page" not in st.session_state:
    st.session_state.page = "upload"

# =========================================================
# PAGE 1: UPLOAD + PROCESS
# =========================================================
if st.session_state.page == "upload":

   st.markdown("""
<h1 style="text-align:center; font-weight:800; color:#e6ddff;">
STUDYBUDDY AI
</h1>
<p style="text-align:center; font-size:18px; color:#b9a7d8;">
Your Study Partner
</p>
""", unsafe_allow_html=True)




    # -------------------------
    # NOTES UPLOAD
    # -------------------------
    # 
st.subheader("📒 Upload Notes")
notes_files = st.file_uploader(
        "Notes (PDF / DOCX / PPTX)",
        type=["pdf", "docx", "pptx"],
        accept_multiple_files=True,
        key="notes"
    )

if notes_files:
        for file in notes_files:
            save_file(file, "notes")
        st.session_state.files_uploaded = True
        st.success("Notes uploaded")

    # -------------------------
    # SYLLABUS UPLOAD
    # -------------------------
st.subheader("📄 Upload Syllabus")
syllabus_file = st.file_uploader(
        "Syllabus (PDF / DOCX)",
        type=["pdf", "docx"],
        key="syllabus"
    )

if syllabus_file:
        save_file(syllabus_file, "syllabus")
        st.session_state.files_uploaded = True
        st.success("Syllabus uploaded")

    # -------------------------
    # PYQ UPLOAD
    # -------------------------
st.subheader("📝 Upload PYQ Papers")
pyq_files = st.file_uploader(
        "PYQ Papers (PDF / DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        key="pyq"
    )

if pyq_files:
        for file in pyq_files:
            save_file(file, "pyq")
        st.session_state.files_uploaded = True
        st.success("PYQ uploaded")

st.divider()

    # -------------------------
    # PROCESS BUTTON
    # -------------------------
if st.session_state.files_uploaded and not st.session_state.kb_built:
        if st.button("🚀 Start Processing"):
            with st.spinner("Building knowledge base..."):
                build_knowledge_base()

            st.session_state.kb_built = True
            st.session_state.page = "options"

    # 🔑 STOP showing upload page immediately
st.rerun()


# =========================================================
# PAGE 2: OPTIONS PAGE
# =========================================================

if st.session_state.page == "options":

    st.markdown(
        "<h2 style='text-align:center; color:#e6ddff;'>Choose a Mode</h2>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("📘  Summary", use_container_width=True):
        st.session_state.page = "summary"
        st.rerun()

    if st.button("❓  Important Questions", use_container_width=True):
        st.session_state.page = "imp_questions"
        st.rerun()

    if st.button("✅  MCQ Test", use_container_width=True):
        st.session_state.page = "mcq"
        st.rerun()

    if st.button("🧠  Mock Test", use_container_width=True):
        st.session_state.page = "mock"
        st.rerun()

    if st.button("⚡  Timed Quiz", use_container_width=True):
        st.session_state.page = "quiz"
        st.rerun()



from logic.rag_engine import retrieve_context
from logic.summary_engine import generate_summary

# =========================================================
# PAGE 3: GENERATE SUMMARY
# =========================================================
if st.session_state.page == "summary":

    st.title("📘 Topic-wise Summary")

    st.write("Enter a topic to generate an exam-oriented summary.")

    topic = st.text_input("Enter topic name")

    if topic:
        with st.spinner("Generating summary from your materials..."):
            # 1. Retrieve relevant content
            context = retrieve_context(topic)

            # 2. Generate summary
            summary = generate_summary(context, topic)

        st.subheader("📝 Summary")
        st.write(summary)

    st.divider()

    if st.button("⬅️ Back to Options"):
        st.session_state.page = "options"
        st.rerun()

from logic.question_engine import generate_important_questions
# =========================================================
# PAGE 4: IMPORTANT QUESTIONS
# =========================================================
if st.session_state.page == "imp_questions":

    st.title("❓ Important Questions with Answers")
    st.write("Generate exam-oriented important questions from your materials.")

    topic = st.text_input("Enter topic name")

    if topic:
        with st.spinner("Generating important questions..."):
            # 1. Retrieve relevant context using RAG
            context = retrieve_context(topic)

        if not context.strip():
            st.error("No relevant content found for this topic.")
        else:
            questions = generate_important_questions(context, topic)
            st.subheader("📌 Important Questions")
            st.write(questions)

    st.divider()

    if st.button("⬅️ Back to Options"):
        st.session_state.page = "options"
        st.rerun()

from logic.mcq_engine import generate_mcqs
if "mcqs" not in st.session_state:
    st.session_state.mcqs = None

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# =========================================================
# PAGE: MCQ TEST
# =========================================================
if st.session_state.page == "mcq":

    st.title("✅ MCQ Test")

    topic = st.text_input("Enter topic name")
    num_q = st.slider("Number of questions", 3, 10, 5)

    # Generate MCQs
    if topic and st.session_state.mcqs is None:
        with st.spinner("Generating MCQs..."):
            context = retrieve_context(topic)

        if not context.strip():
            st.error("No relevant content found.")
        else:
            st.session_state.mcqs = generate_mcqs(context, topic, num_q)
            st.session_state.user_answers = {}

    # Show MCQs
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

    # Results
    if st.session_state.submitted:
        score = 0
        total = len(st.session_state.mcqs)

        st.subheader("📊 Results")

        for i, q in enumerate(st.session_state.mcqs):
            if st.session_state.user_answers.get(i) == q["answer"]:
                score += 1
                st.success(f"Q{i+1}: Correct ✅")
            else:
                st.error(f"Q{i+1}: Wrong ❌ | Correct: {q['answer']}")

        st.markdown(f"## 🏆 Final Score: **{score} / {total}**")

        if score == total:
            st.success("Excellent! Perfect score 🎉")
        elif score >= total * 0.6:
            st.warning("Good job! Revise weak areas.")
        else:
            st.error("Needs improvement. Revise this topic.")

    if st.button("⬅️ Back to Options"):
        st.session_state.page = "options"
        st.rerun()
    
# =========================================================
# PAGE: MOCK TEST
# =========================================================
if st.session_state.page == "mock":

    st.title("🧠 Mock Test")

    topic = st.text_input("Enter topic name")
    num_q = st.slider("Number of questions", 3, 10, 5)

    if "mock_questions" not in st.session_state:
        st.session_state.mock_questions = None

    if topic and st.session_state.mock_questions is None:
        with st.spinner("Generating mock test..."):
            context = retrieve_context(topic)

        if not context.strip():
            st.error("No relevant content found.")
        else:
            st.session_state.mock_questions = generate_mock_questions(
                context, topic, num_q
            )
            st.session_state.mock_context = context

    if st.session_state.mock_questions:
        st.subheader("📄 Questions")
        st.write(st.session_state.mock_questions)

        answers = st.text_area(
            "✍️ Write your answers here (mention question numbers)",
            height=300
        )

        if st.button("📊 Submit Mock Test"):
            with st.spinner("Evaluating your answers..."):
                result = evaluate_mock_answers(
                    st.session_state.mock_context,
                    st.session_state.mock_questions,
                    answers
                )
            st.subheader("📝 Evaluation Result")
            st.write(result)

    if st.button("⬅️ Back to Options"):
        st.session_state.page = "options"
        st.session_state.mock_questions = None
        st.rerun()

# =========================================================
# PAGE: INTERACTIVE QUIZ
# =========================================================
if st.session_state.page == "quiz":

    st.title("⚡ Interactive Quiz")

    topic = st.text_input("Enter topic name")

    # -------------------------
    # INIT STATE
    # -------------------------
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.feedback = None
        st.session_state.start_time = None

    # -------------------------
    # GENERATE QUIZ
    # -------------------------
    if topic and st.session_state.quiz_data is None:
        context = retrieve_context(topic)
        if not context.strip():
            st.error("No relevant content found.")
        else:
            quiz = generate_quiz(context, topic)
            if not quiz:
                st.error("Quiz generation failed.")
            else:
                st.session_state.quiz_data = quiz
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.feedback = None
                st.session_state.start_time = time.time()
                st.rerun()

    # -------------------------
    # SHOW QUESTION
    # -------------------------
    if st.session_state.quiz_data:

        q = st.session_state.quiz_data[st.session_state.quiz_index]

        st.markdown(
            f"### Question {st.session_state.quiz_index + 1} / {len(st.session_state.quiz_data)}"
        )
        st.markdown(f"**{q['question']}**")

        # TIMER
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 30 - elapsed)
        st.warning(f"⏳ Time left: {remaining} seconds")

        # LIVE SCORE
        st.info(f"🏆 Score: {st.session_state.quiz_score}")

        choice = st.radio(
            "Choose your answer:",
            list(q["options"].keys()),
            format_func=lambda x: f"{x}. {q['options'][x]}",
            key=f"quiz_{st.session_state.quiz_index}"
        )

        # -------------------------
        # SUBMIT ANSWER
        # -------------------------
        if st.button("Submit Answer") and st.session_state.feedback is None:
            if choice == q["answer"]:
                st.session_state.feedback = "correct"
                st.session_state.quiz_score += 1
            else:
                st.session_state.feedback = "wrong"

        # -------------------------
        # SHOW FEEDBACK
        # -------------------------
        if st.session_state.feedback:
            if st.session_state.feedback == "correct":
                st.success("Correct ✅")
            else:
                st.error(f"Wrong ❌ | Correct answer: {q['answer']}")

            if st.button("Next Question"):
                st.session_state.feedback = None
                st.session_state.quiz_index += 1
                st.session_state.start_time = time.time()

                if st.session_state.quiz_index >= len(st.session_state.quiz_data):
                    st.session_state.page = "quiz_result"
                st.rerun()
if st.session_state.page == "quiz_result":

    st.title("🏁 Quiz Finished")

    total = len(st.session_state.quiz_data)
    score = st.session_state.quiz_score

    st.metric("Final Score", f"{score} / {total}")

    if score == total:
        st.success("Excellent! Perfect performance 🎉")
    elif score >= total * 0.6:
        st.warning("Good job! Revise weak areas.")
    else:
        st.error("Needs improvement. Keep practicing!")

    if st.button("⬅ Back to Options"):
        st.session_state.page = "options"
        st.session_state.quiz_data = None
        st.rerun()

