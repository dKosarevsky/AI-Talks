from openai.error import AuthenticationError
from pathlib import Path

from src.utils.helpers import api_key_checker, send_ai_request, lang_selector, speech_speed_radio, show_player

import streamlit as st

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "src/styles/.css"
assets_dir = current_dir / "src/assets"
icons_dir = assets_dir / "icons"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "AI Talks"
PAGE_ICON = "🤖"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align: center;'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)
st.markdown("---")


def main() -> None:
    api_key = st.text_input(label="Input OpenAI API key:")
    api_key = api_key_checker(api_key)

    user_text = st.text_area(label="Start your conversation with AI:")
    if st.button("Rerun"):
        st.cache_data.clear()

    if api_key and user_text:
        try:
            completion = send_ai_request(api_key, user_text)
            if st.checkbox(label="Show Full API Response", value=False):
                st.json(completion)
            ai_content = completion.get("choices")[0].get("message").get("content")
            if ai_content:
                st.markdown(ai_content)
                st.markdown("---")

                col1, col2 = st.columns(2)
                with col1:
                    lang_code = lang_selector()
                with col2:
                    is_speech_slow = speech_speed_radio()
                show_player(ai_content, lang_code, is_speech_slow)
        except AuthenticationError as err:
            st.error(err)


if __name__ == "__main__":
    main()
