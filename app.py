import streamlit as st
from dotenv import load_dotenv
from logic_utils import get_num_questions, update_score
from rag_utils import get_collection, retrieve_questions, grade_answer

load_dotenv()

st.set_page_config(page_title="Trivia Time!", page_icon="🎓")
st.title("🎓 Kindergarten Trivia")
st.caption("Answer questions retrieved from our knowledge base!")

# --- Sidebar ---
st.sidebar.header("Settings")
category = st.sidebar.selectbox(
    "Pick a category",
    ["Animals", "Colors", "Shapes", "Numbers"],
)
st.sidebar.caption(f"Questions per game: {get_num_questions()}")

# --- Load ChromaDB collection once ---
@st.cache_resource
def load_collection():
    return get_collection()

collection = load_collection()

# --- Session state init ---
def _start_new_game(cat: str):
    st.session_state.questions = retrieve_questions(collection, cat, get_num_questions())
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.feedback = None
    st.session_state.last_category = cat

if "questions" not in st.session_state:
    _start_new_game(category)

# Restart if category changed
if st.session_state.get("last_category") != category:
    _start_new_game(category)

# --- New Game button ---
if st.sidebar.button("New Game 🔁"):
    _start_new_game(category)
    st.rerun()

# --- Game over screen ---
if st.session_state.status == "done":
    total = get_num_questions()
    score = st.session_state.score
    max_score = total * 10
    st.success(f"Game over! You scored **{score} / {max_score}**.")
    if score == max_score:
        st.balloons()
        st.info("Perfect score! You're a trivia star! 🌟")
    if st.button("Play Again 🔁"):
        _start_new_game(category)
        st.rerun()
    st.stop()

# --- Current question ---
questions = st.session_state.questions
current_q = st.session_state.current_q
q = questions[current_q]

st.progress((current_q) / get_num_questions(), text=f"Question {current_q + 1} of {get_num_questions()}")
st.subheader(q["question"])

# Show previous feedback
if st.session_state.feedback:
    is_correct, msg = st.session_state.feedback
    if is_correct:
        st.success(msg)
    else:
        st.error(msg)
    st.session_state.feedback = None

# --- Answer input ---
user_answer = st.text_input(
    "Your answer:",
    key=f"answer_{current_q}",
    placeholder="Type your answer here...",
)

if st.button("Submit Answer 🚀"):
    if not user_answer.strip():
        st.warning("Please type an answer first!")
    else:
        with st.spinner("Checking your answer..."):
            is_correct, feedback = grade_answer(q["question"], q["answer"], user_answer)

        st.session_state.score = update_score(st.session_state.score, is_correct)
        st.session_state.feedback = (is_correct, feedback)

        next_q = current_q + 1
        if next_q >= get_num_questions():
            st.session_state.status = "done"
        else:
            st.session_state.current_q = next_q

        st.rerun()

# --- Score display ---
st.divider()
st.caption(f"Score: {st.session_state.score} | Category: {category}")
