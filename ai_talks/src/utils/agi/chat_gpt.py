import logging
from typing import List  # NOQA: UP035

import openai
import streamlit as st


@st.cache_data()
def create_gpt_completion(ai_model: str, messages: List[dict]) -> dict:
    try:
        openai.api_key = st.secrets.api_credentials.api_key
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
    logging.info(f"{messages=}")
    completion = openai.ChatCompletion.create(
        model=ai_model,
        messages=messages,
        # stream=True,
        # temperature=0.7,
    )
    logging.info(f"{completion=}")
    return completion
