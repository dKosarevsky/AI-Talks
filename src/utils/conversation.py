import streamlit as st
from openai.error import OpenAIError
from streamlit_chat import message

from src.utils.ai_interaction import send_ai_request
from src.utils.tts import show_player


def clear_chat() -> None:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["messages"] = []
    st.session_state["user_text"] = ""


def get_user_input():
    st.text_area(label=st.session_state.locale.chat_placeholder, value=st.session_state.user_text, key="user_text")


def show_chat_buttons() -> None:
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(st.session_state.locale.chat_run_btn)
        b1.button(st.session_state.locale.chat_rerun_btn, on_click=st.cache_data.clear)
        b2.button(st.session_state.locale.chat_clear_btn, on_click=clear_chat)


def show_chat(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user", avatar_style="micah")
            message("", key=str(i))
            st.markdown(st.session_state["generated"][i])


def show_conversation(user_content: str, model: str, role: str) -> None:
    if st.session_state["messages"]:
        st.session_state["messages"].append({"role": "user", "content": user_content})
    else:
        st.session_state["messages"] = [
            {"role": "system", "content": f"{st.session_state.locale.ai_role_prefix} {role}."},
            {"role": "user", "content": user_content},
        ]
    try:
        completion = send_ai_request(model, st.session_state["messages"])
        ai_content = completion.get("choices")[0].get("message").get("content")
        st.session_state["messages"].append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_chat(ai_content, user_content)
            st.markdown("---")
            show_player(ai_content)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)
