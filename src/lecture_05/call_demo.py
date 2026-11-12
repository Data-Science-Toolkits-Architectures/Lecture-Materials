"""A page that calls the backend, as on the slide "The Page Calls the Backend".

Start the small backend first, then the page, each from this folder:
    uv run uvicorn small_backend:app --port 8000
    BACKEND_URL=http://localhost:8000 uv run streamlit run call_demo.py
"""

import os

import httpx
import streamlit as st

BACKEND_URL = os.environ["BACKEND_URL"]

st.title("Credit decision")

age = st.number_input("Age in years", value=None, step=1)
income = st.number_input("Income per month, CHF", value=None)
utilisation = st.number_input("Utilisation, 0.30 is 30%", value=None)

if st.button("Decide"):
    application = {"age": age, "monthly_income": income, "utilisation": utilisation}
    try:
        answer = httpx.post(f"{BACKEND_URL}/decisions", json=application, timeout=10)
    except httpx.HTTPError:
        st.error("The backend does not answer.")
        st.stop()
    if answer.status_code == 422:
        st.warning("A field is missing or does not fit.")
    elif answer.status_code != 200:
        st.error("The backend failed. Nothing was decided.")
    else:
        st.success(answer.json()["outcome"])
