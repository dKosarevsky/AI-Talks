from streamlit_option_menu import option_menu
from pathlib import Path

from src.utils.lang import en, ru
from src.utils.donates import show_donates
from src.utils.conversation import get_user_input, show_chat_buttons, show_conversation

import streamlit as st

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "src/styles/.css"
assets_dir = current_dir / "src/assets"
icons_dir = assets_dir / "icons"

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
    icons=["flag_en", "flag_ru"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0px",
            "display": "grid",
            "margin": "0!important",
            "background-color": "#2C3333"
        },
        "icon": {"color": "#CBE4DE", "font-size": "14px"},
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
            "margin": "auto",
            "background-color": "#2C3333",
            "height": "30px",
            "width": "7rem",
            "color": "#CBE4DE",
            "border-radius": "5px"
        },
        "nav-link-selected": {
            "background-color": "#2E4F4F",
            "font-weight": "300",
            "color": "#f5f5f5",
            "border": "1px solid #0E8388"
        }
    }
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
    show_donates()
