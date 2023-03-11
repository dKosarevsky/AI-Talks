from typing import List, Dict, Tuple

import streamlit as st
import openai

AI_MODEL_OPTIONS = [
    "gpt-3.5-turbo",
    "gpt-4.0",
]

AI_ROLE_OPTIONS = [
    "helpful assistant",
    "code assistant",
    "code reviewer",
    "text improver",
    "cinema expert",
    "sport expert",
    "online games expert",
    "food recipes expert",
    "English grammar expert",
]


def ai_settings() -> Tuple[str, str]:
    c1, c2 = st.columns(2)
    with c1, c2:
        model = c1.selectbox(label="Select AI Model", options=AI_MODEL_OPTIONS)
        role = c2.selectbox(label="Select AI Role", options=AI_ROLE_OPTIONS)
    return model, role


@st.cache_data()
def send_ai_request(ai_model: str, messages: List[Dict]) -> Dict:
    openai.api_key = st.secrets.api_credentials.api_key
    completion = openai.ChatCompletion.create(
        model=ai_model,
        messages=messages,
    )
    return completion
