from openai import OpenAI
from anthropic import Anthropic

import streamlit as st


def get_api_client(is_open_ai: bool = True):
    try:
        if is_open_ai:
            client = OpenAI(api_key=st.secrets.api_credentials.api_key, organization=st.secrets.api_credentials.api_org)
        else:
            client = Anthropic(api_key=st.secrets.api_credentials.anthropic_api_key)
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
        st.stop()
    return client
