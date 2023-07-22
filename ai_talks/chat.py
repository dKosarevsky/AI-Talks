from pathlib import Path
from random import randrange

import streamlit as st
from src.styles.menu_styles import HEADER_STYLES
from src.utils.back import logout, show_auth_menu
from src.utils.constants import (
    FREQUENCY_PENALTY_KEY,
    PRESENCE_PENALTY_KEY,
    TEMP_KEY,
    TOP_P_KEY,
    USER_TXT_KEY,
)
from src.utils.conversation import clear_chat, get_user_input, show_conversation
from src.utils.lang import en, ru
from streamlit_option_menu import option_menu

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "AI Talks"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-4",
    "gpt-4-32k",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

selected_lang = option_menu(
    menu_title=None,
    options=[LANG_EN, LANG_RU, ],
    icons=["globe2", "translate"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles=HEADER_STYLES
)


# Storing The Context
if "authentication_status" not in st.session_state:
    st.session_state.authentication_status = None
if "locale" not in st.session_state:
    st.session_state.locale = en
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if USER_TXT_KEY not in st.session_state:
    st.session_state.user_text = ""
if "seed" not in st.session_state:
    st.session_state.seed = randrange(10**3)  # noqa: S311
if TEMP_KEY not in st.session_state:
    st.session_state.temperature = 1.
if TOP_P_KEY not in st.session_state:
    st.session_state.top_p = 1.
# if MAX_TOKENS_KEY not in st.session_state:
#     st.session_state.max_tokens = float("inf")
if PRESENCE_PENALTY_KEY not in st.session_state:
    st.session_state.presence_penalty = 0.
if FREQUENCY_PENALTY_KEY not in st.session_state:
    st.session_state.frequency_penalty = 0.
if "costs" not in st.session_state:
    st.session_state.costs = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = []


def show_user_data() -> None:
    with st.sidebar:
        st.markdown(f"{st.session_state.locale.greetings}**{st.session_state.username}** :wave:")
        if st.button(st.session_state.locale.logout):
            logout(st.session_state["applicant-token"])
        st.divider()
        st.markdown(f"[{st.session_state.locale.get_tokens}](https://boosty.to/ai-talks/donate)")


def run_agi() -> None:
    try:
        if st.session_state.username and st.session_state.is_active:
            c1, c2 = st.columns(2)
            with c1, c2:
                c1.selectbox(label=st.session_state.locale.select_placeholder1,
                             key="model", options=AI_MODEL_OPTIONS, on_change=clear_chat)
                role_kind = c2.radio(
                    label=st.session_state.locale.radio_placeholder,
                    options=(st.session_state.locale.radio_text1, st.session_state.locale.radio_text2),
                    horizontal=True,
                    on_change=clear_chat,
                )
            match role_kind:
                case st.session_state.locale.radio_text1:
                    st.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                                 options=st.session_state.locale.ai_role_options)
                case st.session_state.locale.radio_text2:
                    st.text_input(label=st.session_state.locale.select_placeholder3, key="role")

            p1, p2, p3, p4 = st.columns(4)
            p1.number_input(label=TEMP_KEY, min_value=0., max_value=2., key=TEMP_KEY)
            p2.number_input(label=TOP_P_KEY, min_value=0., max_value=2., key=TOP_P_KEY)
            # p3.number_input(label=MAX_TOKENS_KEY, min_value=0., max_value=float("inf"), key=MAX_TOKENS_KEY)
            p3.number_input(label=PRESENCE_PENALTY_KEY, min_value=-2., max_value=2., key=PRESENCE_PENALTY_KEY)
            p4.number_input(label=FREQUENCY_PENALTY_KEY, min_value=-2., max_value=2., key=FREQUENCY_PENALTY_KEY)
            if st.session_state.user_text:
                show_conversation()
                st.session_state.user_text = ""
            get_user_input()
        else:
            st.warning(st.session_state.locale.activate)
    except KeyError:
        st.error("User not found.")


def main():
    match selected_lang:
        case "En":
            st.session_state.locale = en
        case "Ru":
            st.session_state.locale = ru
        case _:
            st.session_state.locale = en
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    if st.session_state.authentication_status is False or st.session_state.authentication_status is None:
        show_auth_menu()
    elif st.session_state.authentication_status:
        show_user_data()
        run_agi()


if __name__ == "__main__":
    main()
