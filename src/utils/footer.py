from pathlib import Path

import streamlit as st

from src.utils.helpers import render_svg


def show_info(icon: Path) -> None:
    st.markdown(f"""
        ### :page_with_curl: {st.session_state.locale.footer_title}
        - {render_svg(icon)} [{st.session_state.locale.footer_chat}](https://t.me/talks_ai)
        - {render_svg(icon)} [{st.session_state.locale.footer_channel}](https://t.me/talks_aii)
    """, unsafe_allow_html=True)


def show_donates() -> None:
    st.markdown(f"""
        ### :moneybag: {st.session_state.locale.donates}
        **{st.session_state.locale.donates1}:**
        - [CloudTips (Tinkoff)](https://pay.cloudtips.ru/p/eafa15b2)

        **{st.session_state.locale.donates2}:**
        - [Buy Me A Coffee](https://www.buymeacoffee.com/aitalks)
        - [ko-fi](https://ko-fi.com/ai_talks)
        - [PayPal](https://www.paypal.com/paypalme/aitalks)

        **Crypto:**
        - USD Tether (USDT TRC20) ```TMQ5RiyQ7bv3XjB6Wf6JbPHVrGkhBKtmfA```
        - Toncoin (TON) ```UQDbnx17N2iOmxfQF0k55QScDMB0MHL9rsq-iGB93RMqDhIH```
    """)
