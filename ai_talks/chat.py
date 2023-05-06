import time
from pathlib import Path
from random import randrange

import requests
import streamlit as st
from src.styles.menu_styles import HEADER_STYLES
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


def show_auth_menu() -> None:
    applicant_token = ""
    if "applicant-token" in st.session_state:
        applicant_token = st.session_state["applicant-token"]
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
            login(applicant_token)
        case "register":
            register(applicant_token)
        case _:
            login(applicant_token)


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


def logout(applicant_token: str) -> None:
    if applicant_token:
        with st.form("my_form"):
            st.write("Do you want to log out?")
            submit_res = st.form_submit_button(label="Logout here")
            if submit_res:
                if "applicant-token" in st.session_state:
                    del st.session_state["applicant-token"]
                st.write("You are now logged out!")
    else:
        st.write("You are now logged out!")


def show_user_data() -> None:
    with st.sidebar:
        st.markdown(f"Welcome back, **{st.session_state.name}**!")
        if st.button("Logout"):
            logout(st.session_state["applicant-token"])
        st.divider()
        if st.sidebar.checkbox("Show Reset Password Menu"):
            ...
        st.divider()
        if st.sidebar.checkbox("Show Update User Details"):
            ...
        st.divider()
        try:
            st.code(f"Tokens: {st.secrets.tokens[st.session_state.username]}")
        except KeyError:
            st.error("You need to activate your account. Write to Admin in telegram.")


def login(applicant_token: str) -> None:
    if applicant_token:
        st.session_state.authentication_status = True
    else:
        with st.form("my_form"):
            email = st.text_input(label="email")
            password = st.text_input(label="password", type="password")
            submit_res = st.form_submit_button(label="Login")
            if submit_res:
                st.write("login clicked!")
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post(url=st.secrets.back.base_url + "api_auth/", headers=headers,  # noqa: S113
                                         json={"email": email, "password": password})
                if response.status_code == 200:
                    response_json = response.json()
                    applicant_token = response_json["token"]
                    if applicant_token:
                        st.session_state.key = "applicant-token"
                        st.session_state["applicant-token"] = applicant_token
                        st.experimental_rerun()
                else:
                    st.error(f"Error: {response.text}. Status code: {response.status_code}")


def register(applicant_token: str) -> None:
    if applicant_token:
        with st.form("my_form"):
            st.write("You need to first logout before registering!")
            submit_res = st.form_submit_button(label="Logout here")
            if submit_res:
                st.write("You are now logged out!")
                del st.session_state["applicant-token"]
                time.sleep(3)
                st.experimental_rerun()
    else:
        with st.form("my_form"):
            email = st.text_input(label="email")
            username = st.text_input(label="username")
            password = st.text_input(label="password", type="password")
            submit_res = st.form_submit_button(label="Register")
            if submit_res:
                st.write("registered clicked!")
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.post(url=st.secrets.back.base_url + "api_register/", headers=headers,  # noqa: S113
                                         json={"email": email, "username": username, "password": password})
                if response.status_code == 200:
                    st.experimental_rerun()
                else:
                    st.error(f"Error: {response.text}. Status code: {response.status_code}")


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
    if st.session_state.authentication_status is False or st.session_state.authentication_status is None:
        show_auth_menu()
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
