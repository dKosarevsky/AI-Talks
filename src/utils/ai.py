from typing import Dict, Tuple

import streamlit as st
import openai

AI_MODEL_OPTIONS = [
    "gpt-3.5-turbo",
]

AI_ROLE_OPTIONS = [
    "helpful assistant",
    "code assistant",
    "text improver",
    "cinema expert",
    "sport expert",
    "online games expert",
    "expert in delicious food recipes",
    "expert in healthy food recipes",
]


def ai_settings() -> Tuple[str, str]:
    c1, c2 = st.columns(2)
    with c1, c2:
        model = c1.selectbox(label="Select AI model", options=AI_MODEL_OPTIONS)
        role = c2.selectbox(label="Select AI role", options=AI_ROLE_OPTIONS)
    return model, role


@st.cache_data()
def send_ai_request(user_text: str, ai_model: str, ai_role: str) -> Dict:
    openai.api_key = st.secrets.api_credentials.api_key
    completion = openai.ChatCompletion.create(
        model=ai_model,
        messages=[
            {"role": "system", "content": f"You are a {ai_role}."},
            {
                "role": "user",
                "content": user_text
            }
        ]
    )
    return completion
