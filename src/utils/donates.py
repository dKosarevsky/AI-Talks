import streamlit as st


def show_donates() -> None:
    st.markdown("---")
    st.markdown(f"""
        ### :moneybag: {st.session_state.locale.donates}
        **{st.session_state.locale.donates1}:**
        - [CloudTips (Tinkoff)](https://pay.cloudtips.ru/p/eafa15b2)

        **{st.session_state.locale.donates2}:**
        - [Buy Me A Coffee](https://www.buymeacoffee.com/aitalks)
        - [ko-fi](https://ko-fi.com/ai_talks)
        - [PayPal](https://www.paypal.com/paypalme/aitalks)
    """)
