from openai.error import AuthenticationError
from pathlib import Path
from gtts import gTTS, lang
from io import BytesIO

from src.utils.helpers import get_dict_key

import streamlit as st
import openai

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

api_key = st.text_input(label="Input OpenAI API key:")
if api_key == "ZVER":
    api_key = st.secrets.api_credentials.api_key

user_text = st.text_area(label="Start your conversation with AI:")

if api_key and user_text:
    openai.api_key = api_key
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )
        if st.checkbox(label="Show Full API Response", value=False):
            st.json(completion)

        ai_content = completion.get("choices")[0].get("message").get("content")

        if ai_content:
            st.markdown(ai_content)
            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                languages = lang.tts_langs()
                lang_options = list(lang.tts_langs().values())
                default_index = lang_options.index("Russian")
                lang_name = st.selectbox(
                    label="Select speech language",
                    options=lang_options,
                    index=default_index
                )
                lang_code = get_dict_key(languages, lang_name)
            with col2:
                speed_options = {
                    "Normal": False,
                    "Slow": True
                }
                speed_speech = st.radio(
                    label="Select speech speed",
                    options=speed_options.keys(),
                )
                is_speech_slow = speed_options.get(speed_speech)
            if lang_code and is_speech_slow is not None:
                sound_file = BytesIO()
                tts = gTTS(text=ai_content, lang=lang_code, slow=is_speech_slow)
                tts.write_to_fp(sound_file)
                st.write("Push play to hear sound of AI:")
                st.audio(sound_file)
    except AuthenticationError as err:
        st.error(err)
