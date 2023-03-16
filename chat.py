from openai.error import OpenAIError
from pathlib import Path

from src.utils.ai import ai_settings, send_ai_request
from src.utils.tts import show_player
from src.utils.conversation import get_user_input, clear_chat, show_conversation

import streamlit as st

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "src/styles/.css"
assets_dir = current_dir / "src/assets"
icons_dir = assets_dir / "icons"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "AI Talks"
PAGE_ICON = "🤖"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align: center;'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)
st.markdown("---")

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
    b1, b2 = st.columns(2)
    with b1, b2:
        b1.button("Rerun", on_click=st.cache_data.clear)
        b2.button("Clear Conversation", on_click=clear_chat)

    model, role = ai_settings()

    if user_content:
        if st.session_state["messages"]:
            st.session_state["messages"].append({"role": "user", "content": user_content})
        else:
            st.session_state["messages"] = [
                {"role": "system", "content": f"You are a {role}."},
                {"role": "user", "content": user_content},
            ]
        try:
            completion = send_ai_request(model, st.session_state["messages"])
            ai_content = completion.get("choices")[0].get("message").get("content")
            st.session_state["messages"].append({"role": "assistant", "content": ai_content})
            if ai_content:
                show_conversation(ai_content, user_content)
                st.markdown("---")
                show_player(ai_content)
        except (OpenAIError, UnboundLocalError) as err:
            st.error(err)


if __name__ == "__main__":
    main()
    st.image("assets/ai.jpg")
