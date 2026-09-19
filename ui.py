# Beautiful UI for QueryPilot.
import streamlit as st
from clarify import check_question
from graph import run_q

# Page look.
st.set_page_config(page_title="QueryPilot", page_icon="🧭", layout="centered")

# Light CSS for shadow and buttons.
st.markdown("""
<style>
.ex {box-shadow: 0 2px 8px rgba(0,0,0,0.12); border-radius:10px; padding:8px; margin:4px 0;}
.stButton>button {border-radius:10px; width:100%;}
</style>
""", unsafe_allow_html=True)

st.title("🧭 QueryPilot")
st.caption("Ask in English, get SQL.")

# Examples with light shadow.
st.subheader("Try examples")
examples = [
    "last 30 days city-wise orders?",
    "where are my orders?",
    "show sales",
]
for e in examples:
    st.markdown('<div class="ex">', unsafe_allow_html=True)
    if st.button(e, key=e):
        st.session_state["q"] = e
    st.markdown('</div>', unsafe_allow_html=True)

# Input.
q = st.text_input("Ask question", key="q")

# Submit saves question.
if st.button("Submit ✨"):
    st.session_state["done"] = q

# Work after submit, no nested button.
if st.session_state.get("done"):
    dq = st.session_state["done"]
    status, msg, opts = check_question(dq)
    if status == "ok":
        st.success("Clear question.")
        st.write(run_q(dq))
    elif status == "need_clarification":
        st.warning(msg)
        choice = st.radio("Select any one", opts, key="pick")
        if st.button("Run"):
            st.write(run_q(dq + " " + choice))
    else:
        st.warning(msg)
        if st.button("Yes, run"):
            st.write(run_q(dq))