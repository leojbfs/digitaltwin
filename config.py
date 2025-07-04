import streamlit as st

DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]
DB_NAME = st.secrets["DB_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")
OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
