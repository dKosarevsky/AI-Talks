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
                stream=True,
            )
            # Handle streaming response
            content = ""
            for chunk in completion:
                if chunk.choices and hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
                    content += chunk.choices[0].delta.content

            # Get usage information from the last chunk
            usage = None
            if hasattr(chunk, 'usage'):
                usage = chunk.usage

            logging.info(f"Collected content: {content}")
            return content, usage
        except OpenAIError as err:
            st.error(err)
            st.stop()
    else:
        # https://github.com/anthropics/anthropic-sdk-python
        try:
            message = client.messages.create(
                max_tokens=32_000,
                messages=messages,
                model=ai_model,
                stream=True,
            )
            # Handle streaming response
            content = ""
            for chunk in message:
                if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text') and chunk.delta.text:
                    content += chunk.delta.text
                elif hasattr(chunk, 'content') and chunk.content and len(chunk.content) > 0:
                    for content_block in chunk.content:
                        if hasattr(content_block, 'text'):
                            content += content_block.text

            logging.info(f"Collected content: {content}")
            return content, None
        except (AnthropicError, ValueError) as err:
            st.error(err)
            st.stop()
