from pathlib import Path
from random import randrange

import streamlit as st
import yaml
from src.styles.menu_styles import HEADER_STYLES
from src.utils.conversation import clear_chat, get_user_input, show_conversation
from src.utils.lang import en, ru
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
from yaml.loader import SafeLoader

# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "src/styles/.css"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "AI Talks"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
LANG_RU: str = "Ru"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-3.5-turbo",
    "gpt-4",
    # "gpt-4-32k",
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


def show_login_menu() -> None:
    auth = option_menu(
        menu_title=None,
        options=["login", "register", ],
        icons=["door-open", "door-closed"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles=HEADER_STYLES
    )
    match auth:
        case "login":
            login()
        case "register":
            register()
        case _:
            login()


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
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "seed" not in st.session_state:
    st.session_state.seed = randrange(10**3)  # noqa: S311
if "costs" not in st.session_state:
    st.session_state.costs = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = []


def update_config() -> None:
    with open("./.streamlit/cfg.yaml", "w") as file:
        yaml.dump(st.session_state.config, file, default_flow_style=False)


def show_user_data() -> None:
    with st.sidebar:
        st.markdown(f"Welcome back, **{st.session_state.name}**!")
        st.session_state.authenticator.logout("Logout", "sidebar")
        st.divider()
        if st.sidebar.checkbox("Show Reset Password Menu"):
            try:
                if st.session_state.authenticator.reset_password(st.session_state.username, "Reset password"):
                    update_config()
                    st.success("Password modified successfully")
            except Exception as e:
                st.error(e)
        st.divider()
        if st.sidebar.checkbox("Show Update User Details"):
            try:
                if st.session_state.authenticator.update_user_details(st.session_state.username, "Update user details"):
                    update_config()
                    st.success("Entries updated successfully")
            except Exception as e:
                st.error(e)
        st.divider()
        try:
            st.code(f"Tokens: {st.secrets.tokens[st.session_state.username]}")
        except KeyError:
            st.error("You need to activate your account. Write to Admin in telegram.")


def make_authenticator() -> None:
    with open("./.streamlit/cfg.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)  # noqa: S506
    authenticator = Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"]
    )
    st.session_state.authenticator = authenticator
    st.session_state.config = config


def login() -> None:
    st.session_state.authenticator.login("Login", "main")


def register() -> None:
    try:
        if st.session_state.authenticator.register_user("Register user", preauthorization=False):
            update_config()
            st.success("User registered successfully")
    except Exception as e:
        st.error(e)


def run_agi() -> None:
    try:
        if st.session_state.username and st.secrets.is_active[st.session_state.username]:
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

            if st.session_state.user_text:
                show_conversation()
                st.session_state.user_text = ""
            get_user_input()
        else:
            st.warning("User not found.")
    except KeyError:
        st.error("You need to activate your account. Write to Admin in telegram.")


def main():
    match selected_lang:
        case "En":
            st.session_state.locale = en
        case "Ru":
            st.session_state.locale = ru
        case _:
            st.session_state.locale = en
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.locale.title}</h1>", unsafe_allow_html=True)
    make_authenticator()
    if st.session_state.authentication_status is False or st.session_state.authentication_status is None:
        show_login_menu()
    elif st.session_state.authentication_status:
        show_user_data()
        run_agi()
    elif st.session_state.authentication_status is None:
        st.warning("Please enter your username and password")
        st.stop()
    elif not st.session_state.authentication_status:
        st.error("Username/password is incorrect")
        st.stop()


if __name__ == "__main__":
    main()
