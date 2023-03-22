from typing import List

import openai
import streamlit as st


@st.cache_data()
def send_ai_request(ai_model: str, messages: List[dict]) -> dict:
    openai.api_key = st.secrets.api_credentials.api_key
    import logging
    logging.warning("messages:")
    logging.warning(messages)
    completion = openai.ChatCompletion.create(
        model=ai_model,
        messages=messages,
    )
    logging.warning("completion:")
    logging.warning(completion)
    return completion
