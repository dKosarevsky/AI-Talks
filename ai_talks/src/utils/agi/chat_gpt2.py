import logging
import streamlit as st

from typing import List  # NOQA: UP035

from openai.types import CompletionUsage
from openai import OpenAIError
from tenacity import retry, stop_after_attempt

from anthropic import AnthropicError

from .api_utils import get_api_client


@st.cache_data()
@retry(stop=stop_after_attempt(3))
def create_llm_content(ai_model: str, messages: List[dict], is_open_ai: bool) -> tuple[str, CompletionUsage | None]:
    client = get_api_client(is_open_ai=is_open_ai)
    logging.info(f"{messages=}")
    if is_open_ai:
        # https://platform.openai.com/docs/api-reference/chat/create
        try:
            completion = client.chat.completions.create(
                model=ai_model,
                messages=messages,
                temperature=st.session_state.temperature,
                n=1,
                user=st.session_state.username,
                # stream=True,
            )
        except OpenAIError as err:
            st.error(err)
            st.stop()
        logging.info(f"{completion=}")
        return completion.choices[0].message.content, completion.usage
    else:
        # https://github.com/anthropics/anthropic-sdk-python
        try:
            message = client.messages.create(
                max_tokens=32_000,
                messages=messages,
                model=ai_model,
                stream=True,
            )
            logging.info(f"{message=}")
            return message.content[0].text, None
        except (AnthropicError, ValueError) as err:
            st.error(err)
            st.stop()
