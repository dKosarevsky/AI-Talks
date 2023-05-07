import base64
import os
import random
from pathlib import Path

import streamlit as st
from requests import exceptions, get
from requests.auth import HTTPBasicAuth


def get_back_auth() -> HTTPBasicAuth:
    return HTTPBasicAuth(st.secrets.back.usr, st.secrets.back.pwd)


def render_svg(svg: Path) -> str:
    """Renders the given svg string."""
    with open(svg) as file:
        b64 = base64.b64encode(file.read().encode("utf-8")).decode("utf-8")
        return f"<img src='data:image/svg+xml;base64,{b64}'/>"


def get_files_in_dir(path: Path) -> list[str]:
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files


def get_random_img(img_names: list[str]) -> str:
    return random.choice(img_names)  # noqa: S311


def get_balance() -> float:
    session_tkn = st.secrets.api_credentials.open_ai_session
    if not session_tkn:
        return -1
    try:
        data = get(  # noqa: S113
            url="https://api.openai.com/dashboard/billing/credit_grants",
            headers={"Authorization": f"Bearer {session_tkn}"}
        ).json()["grants"]["data"][0]
        return (data["grant_amount"] - data["used_amount"]) / data["grant_amount"]
    except (KeyError, exceptions.RequestException) as e:
        st.error(f"Getting Balance Error: {e}")
        return -1


def show_balance() -> None:
    balance = get_balance()
    if balance != -1:
        ln, pr = st.columns([1, 4])
        with ln, pr:
            ln.text(st.session_state.locale.balance_handler)
            pr.progress(balance)
