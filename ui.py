# Simple UI with buttons.
import streamlit as st
from clarify import check_question
from graph import run_q

# Title.
st.title("QueryPilot")

# Input box.
q = st.text_input("Ask question")

# Check as soon as question is typed.
if q:
    status, msg, opts = check_question(q)
    # Clear question goes direct.
    if status == "ok":
        if st.button("Run"):
            st.write(run_q(q))
    # Unclear shows choice + one run button.
    elif status == "need_clarification":
        st.warning(msg)
        choice = st.radio("Choose", opts)
        if st.button("Run with choice"):
            st.write(run_q(q + " " + choice))
    # Sensitive needs yes.
    else:
        st.warning(msg)
        if st.button("yes-run"):
            st.write(run_q(q))