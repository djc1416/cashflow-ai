import streamlit as st

from translations import TRANSLATIONS

st.set_page_config(
    page_title="CashFlow AI",

)

language = st.selectbox(
    "Idioma / Language",
    options=["es", "en"],
    format_func=lambda x: (
        "Español" if x == "es" else "English"
    ),
)

texts = TRANSLATIONS[language]

st.title(texts["page_title"])
st.write(texts["welcome"])
