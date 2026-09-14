# Simple UI with buttons.
import streamlit as st
from clarify import check_question
from graph import run_q

# Title.
st.title("QueryPilot")

# Input box.
q = st.text_input("Ask question")

# Button to run.
if st.button("Run"):
    status, msg, opts = check_question(q)
    # Clear question goes to graph.
    if status == "ok":
        st.write(run_q(q))
    # Unclear question shows buttons.
    else:
        st.warning(msg)
        for o in opts:
            st.button(o)