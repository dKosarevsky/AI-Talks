from streamlit_option_menu import option_menu
from pathlib import Path

from src.styles.menu_styles import HEADER_STYLES, FOOTER_STYLES
from src.utils.lang import en, ru
from src.utils.footer import show_donates, show_info
from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation

import streamlit as st

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "src/styles/.css"
assets_dir = current_dir / "assets"
icons_dir = assets_dir / "icons"
tg_svg = icons_dir / "telegram.svg"
tg_svg = icons_dir / "tg.svg"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "AI Talks"
PAGE_ICON = "🤖"
AI_MODEL_OPTIONS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
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
    default_index=1,
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
    user_content = get_user_input()
    show_chat_buttons()

    c1, c2 = st.columns(2)
    with c1, c2:
        model = c1.selectbox(label=st.session_state.locale.select_placeholder1, options=AI_MODEL_OPTIONS)
        role = c2.selectbox(label=st.session_state.locale.select_placeholder2,
                            options=st.session_state.locale.ai_role_options)

    if user_content:
        show_conversation(user_content, model, role)


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
    st.image("assets/ai.jpg")
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
        case "Info":
            show_info(tg_svg)
        case "Donates":
            show_donates()
        case _:
            show_info(tg_svg)
