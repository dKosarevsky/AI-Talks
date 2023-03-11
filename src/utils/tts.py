from typing import Any, Dict, Optional
from gtts import gTTS, gTTSError, lang
from io import BytesIO

import streamlit as st

DEFAULT_SPEECH_LANG = "English"


def get_dict_key(dictionary: Dict, value: Any) -> Optional[Any]:
    for key, val in dictionary.items():
        if val == value:
            return key


def lang_selector() -> str:
    languages = lang.tts_langs()
    lang_options = list(lang.tts_langs().values())
    default_index = lang_options.index(DEFAULT_SPEECH_LANG)
    lang_name = st.selectbox(
        label="Select Speech Language",
        options=lang_options,
        index=default_index
    )
    return get_dict_key(languages, lang_name)


def speech_speed_radio() -> bool:
    speed_options = {
        "Normal": False,
        "Slow": True
    }
    speed_speech = st.radio(
        label="Select Speech Speed",
        options=speed_options.keys(),
    )
    return speed_options.get(speed_speech)


def show_player(ai_content: str) -> None:
    sound_file = BytesIO()
    col1, col2 = st.columns(2)
    with col1:
        lang_code = lang_selector()
    with col2:
        is_speech_slow = speech_speed_radio()
    try:
        tts = gTTS(text=ai_content, lang=lang_code, slow=is_speech_slow)
        tts.write_to_fp(sound_file)
        st.write("To Hear The Voice Of AI, Press Play.")
        st.audio(sound_file)
    except gTTSError as err:
        st.error(err)
