import logging
from typing import List  # NOQA: UP035

import openai
from openai import OpenAI

import streamlit as st
from tenacity import retry, stop_after_attempt


@st.cache_data()
@retry(stop=stop_after_attempt(3))
def create_gpt_completion(ai_model: str, messages: List[dict]) -> dict:
    try:
        client = OpenAI(api_key=st.secrets.api_credentials.api_key, organization=st.secrets.api_credentials.api_org)
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
        st.stop()
    logging.info(f"{messages=}")
    # https://platform.openai.com/docs/api-reference/chat/create
    completion = client.chat.completions.create(
        model=ai_model,
        messages=messages,
        temperature=st.session_state.temperature,
        top_p=st.session_state.top_p,
        # max_tokens=st.session_state.max_tokens,
        n=1,
        stop="",
        presence_penalty=st.session_state.presence_penalty,
        frequency_penalty=st.session_state.frequency_penalty,
        # logit_bias={},
        user=st.session_state.username,
        # stream=True,
        # functions: functions,
        # function_call: "auto",
    )
    logging.info(f"{completion=}")
    return completion
