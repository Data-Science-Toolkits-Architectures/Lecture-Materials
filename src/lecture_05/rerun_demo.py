"""Streamlit runs the whole script again on every click.

Run it from this folder with:
    uv run streamlit run rerun_demo.py

Then click Decide a few times, type into the field, and watch both counters.
"""

import streamlit as st

st.title("Credit decision")

# A normal variable starts again on every run.
runs_this_time = 0
runs_this_time += 1

# What must survive a run goes into session_state.
if "runs" not in st.session_state:
    st.session_state.runs = 0
st.session_state.runs += 1

if "clicks" not in st.session_state:
    st.session_state.clicks = 0

# value=None keeps the field empty. Without it, Streamlit fills in 0.
age = st.number_input("Age in years", value=None, step=1)

if st.button("Decide"):
    st.session_state.clicks += 1

st.write("Decide pressed", st.session_state.clicks, "times")
st.write("The age field holds", age)

st.divider()
st.caption(
    f"The script has run {st.session_state.runs} times since you opened the page. "
    f"The normal variable says {runs_this_time}, every time."
)
