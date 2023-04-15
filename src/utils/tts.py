from io import BytesIO

import streamlit as st
from gtts import gTTS, gTTSError


def show_audio_player(ai_content: str) -> None:
    sound_file = BytesIO()
    try:
        tts = gTTS(text=ai_content, lang=st.session_state.locale.lang_code)
        tts.write_to_fp(sound_file)
        st.write(st.session_state.locale.stt_placeholder)
        st.audio(sound_file)
    except gTTSError as err:
        st.error(err)
