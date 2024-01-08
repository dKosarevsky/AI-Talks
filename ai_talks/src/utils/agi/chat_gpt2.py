import logging
import streamlit as st

from typing import List  # NOQA: UP035

from openai.types.chat import ChatCompletion
from tenacity import retry, stop_after_attempt

from .api_utils import get_api_client


@st.cache_data()
@retry(stop=stop_after_attempt(3))
def create_gpt_completion(ai_model: str, messages: List[dict]) -> ChatCompletion:
    client = get_api_client()
    logging.info(f"{messages=}")
    # https://platform.openai.com/docs/api-reference/chat/create
    completion = client.chat.completions.create(
        model=ai_model,
        messages=messages,
        temperature=st.session_state.temperature,
        n=1,
        user=st.session_state.username,
        # stream=True,
    )
    logging.info(f"{completion=}")
    return completion
