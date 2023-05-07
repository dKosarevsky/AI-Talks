import time

import streamlit as st
from requests import exceptions, post
from streamlit_option_menu import option_menu

from ..styles.menu_styles import HEADER_STYLES
from .constants import HEADERS
from .helpers import get_back_auth


def logout(applicant_token: str) -> None:
    if applicant_token:
        st.session_state["applicant-token"] = ""
    st.session_state.authentication_status = False
    st.session_state.username = ""
    st.experimental_rerun()


def login(applicant_token: str) -> None:
    if applicant_token:
        st.session_state.authentication_status = True
    else:
        with st.form("my_form"):
            username = st.text_input(label="username")
            password = st.text_input(label="password", type="password")
            data = {"username": username, "password": password}
            if st.form_submit_button(label="Login"):
                with st.spinner("login..."):
                    try:
                        response = post(url=st.secrets.back.base_url + "auth/", headers=HEADERS,  # noqa: S113
                                        json=data, auth=get_back_auth())
                        if response.status_code == 200:
                            response_json = response.json()
                            applicant_token = response_json["token"]
                            st.session_state.username = response_json["username"]
                            st.session_state.user_tokens = response_json["ai_tokens"]
                            if applicant_token:
                                st.session_state.key = "applicant-token"
                                st.session_state["applicant-token"] = applicant_token
                                st.session_state.authentication_status = True
                                st.experimental_rerun()
                        elif response.status_code in range(500, 512):
                            st.error(f"Server Error. Status code: {response.status_code}")
                        else:
                            st.error(f"Error: {response.text}. Status code: {response.status_code}")
                    except exceptions.RequestException as err:
                        st.error(f"Request Error: {err}")


def register(applicant_token: str) -> None:
    if applicant_token:
        with st.form("my_form"):
            st.write("You need to first logout before registering!")
            if st.form_submit_button(label="Logout here"):
                st.write("You are now logged out!")
                del st.session_state["applicant-token"]
                time.sleep(3)
                st.experimental_rerun()
    else:
        with st.form("my_form"):
            telegram = st.text_input(label="telegram")
            email = st.text_input(label="email")
            username = st.text_input(label="username")
            password = st.text_input(label="password", type="password")
            data = {"telegram": telegram, "email": email, "username": username, "password": password}
            if st.form_submit_button(label="Register"):
                with st.spinner("registration..."):
                    try:
                        response = post(url=st.secrets.back.base_url + "register/", headers=HEADERS,  # noqa: S113
                                        json=data, auth=get_back_auth())
                        if response.status_code == 200:
                            st.experimental_rerun()
                        elif response.status_code in range(500, 512):
                            st.error(f"Server Error. Status code: {response.status_code}")
                        else:
                            st.error(f"Error: {response.text}. Status code: {response.status_code}")
                    except exceptions.RequestException as err:
                        st.error(f"Request Error: {err}")


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
