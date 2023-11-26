from openai import OpenAI

import streamlit as st


def get_api_client():
    try:
        client = OpenAI(api_key=st.secrets.api_credentials.api_key, organization=st.secrets.api_credentials.api_org)
    except (KeyError, AttributeError):
        st.error(st.session_state.locale.empty_api_handler)
        st.stop()
    return client
