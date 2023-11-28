import logging
import streamlit as st

from typing import List  # NOQA: UP035
from tenacity import retry, stop_after_attempt

from .api_utils import get_api_client


@st.cache_data()
@retry(stop=stop_after_attempt(3))
def create_gpt_completion(ai_model: str, messages: List[dict]) -> dict:
    client = get_api_client()
    logging.info(f"{messages=}")
    # https://platform.openai.com/docs/api-reference/chat/create
    completion = client.chat.completions.create(
        model=ai_model,
        messages=messages,
        temperature=st.session_state.temperature,
        # top_p=st.session_state.top_p,
        # max_tokens=st.session_state.max_tokens,
        n=1,
        # stop="",
        # presence_penalty=st.session_state.presence_penalty,
        # frequency_penalty=st.session_state.frequency_penalty,
        user=st.session_state.username,
        # stream=True,
    )
    logging.info(f"{completion=}")
    return completion
