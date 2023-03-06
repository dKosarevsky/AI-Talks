from typing import Any, Dict, Optional
from gtts import gTTS, lang
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
        label="Select speech language",
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
        label="Select speech speed",
        options=speed_options.keys(),
    )
    return speed_options.get(speed_speech)


def show_player(ai_content: str, lang_code: str, is_speech_slow: bool) -> None:
    sound_file = BytesIO()
    tts = gTTS(text=ai_content, lang=lang_code, slow=is_speech_slow)
    tts.write_to_fp(sound_file)
    st.write("To hear the voice of AI, press the play button.")
    st.audio(sound_file)
