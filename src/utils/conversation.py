import streamlit as st
from streamlit_chat import message


def clear_chat() -> None:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["messages"] = []
    st.session_state["user_text"] = ""


def get_user_input() -> str:
    user_text = st.text_area(label="Start Your Conversation With AI:", key="user_text")
    return user_text


def show_conversation(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            st.markdown(st.session_state["generated"][i])
            # message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user", avatar_style="micah")
