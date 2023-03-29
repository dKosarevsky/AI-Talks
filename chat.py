from streamlit_option_menu import option_menu
from pathlib import Path

from src.styles.menu_styles import HEADER_STYLES, FOOTER_STYLES
from src.utils.lang import en, ru
from src.utils.footer import show_donates, show_info
from src.utils.helpers import get_random_img, get_files_in_dir
from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation

import streamlit as st

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "src/styles/.css"
assets_dir = current_dir / "assets"
icons_dir = assets_dir / "icons"
img_dir = assets_dir / "img"
tg_svg = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "AI Talks"
PAGE_ICON = "🤖"
AI_MODEL_OPTIONS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
    "bard",
]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

selected_lang = option_menu(
    menu_title=None,
    options=["En", "Ru", ],
    icons=["globe2", "globe"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles=HEADER_STYLES
)

# Storing The Context
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "user_text" not in st.session_state:
    st.session_state["user_text"] = ""


def main() -> None:
    if st.session_state.user_text:
        show_conversation()
        st.session_state.user_text = ""

    c1, c2, c3 = st.columns(3)
    with c1, c2:
        c1.selectbox(label=st.session_state.locale.select_placeholder1, key="model", options=AI_MODEL_OPTIONS)
        role_kind = c2.radio("Role Kind", ("Select", "Create"), horizontal=True)
        match role_kind:
            case "Select":
                c3.selectbox(label=st.session_state.locale.select_placeholder2, key="role",
                             options=st.session_state.locale.ai_role_options)
            case "Create":
                c3.text_input(label=st.session_state.locale.select_placeholder3, key="role")

    get_user_input()
    show_chat_buttons()


if __name__ == "__main__":
    match selected_lang:
        case "En":
            st.session_state.locale = en
        case "Ru":
            st.session_state.locale = ru
        case _:
            locale = en
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    main()
    st.markdown("---")
    st.image(f"{img_dir}/{get_random_img(get_files_in_dir(img_dir))}")
    st.markdown("---")
    selected_footer = option_menu(
        menu_title=None,
        options=[st.session_state.locale.footer_option1, st.session_state.locale.footer_option2],
        icons=["info-circle", "piggy-bank"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=FOOTER_STYLES
    )
    st.markdown("---")
    match selected_footer:
        case st.session_state.locale.footer_option1:
            show_info(tg_svg)
        case st.session_state.locale.footer_option2:
            show_donates()
        case _:
            show_info(tg_svg)
