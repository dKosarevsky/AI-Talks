from random import randrange

import streamlit as st
from openai import APIError
from openai.types import CompletionUsage
from streamlit_chat import message

from .agi.chat_gpt2 import create_gpt_completion
from .back import debit_tokens
from .constants import USER_TXT_KEY, AIModels


def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.user_text = ""
    st.session_state.seed = randrange(10**8)  # noqa: S311
    st.session_state.costs = []
    st.session_state.total_tokens = []
    st.session_state.temperature = 1.


def show_text_input() -> None:
    st.text_area(label=st.session_state.locale.chat_placeholder, key=USER_TXT_KEY)


def get_user_input():
    with st.form(key="user_input"):
        st.text_area(label=st.session_state.locale.chat_placeholder, key=USER_TXT_KEY)
        st.form_submit_button(label=st.session_state.locale.chat_run_btn, disabled=st.session_state.user_tokens <= 0)
    _, b1, b2 = st.columns(3)
    with b1, b2:
        b1.button(label=st.session_state.locale.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.locale.chat_save_btn,
            data="\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )
    st.code(f"{st.session_state.locale.available_tokens}{st.session_state.user_tokens}")
    st.warning(st.session_state.locale.need_tokens) if st.session_state.user_tokens <= 0 else None


def show_chat(ai_content: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.past.append(st.session_state.user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            message(st.session_state.past[i], is_user=True, key=str(i) + "_user", seed=st.session_state.seed)
            message(st.session_state.generated[i], key=str(i), seed=st.session_state.seed)
            # st.markdown(st.session_state.generated[i])
            st.caption(f"""
                {st.session_state.locale.tokens_count}{st.session_state.total_tokens[i]} |
                {st.session_state.locale.message_cost}{st.session_state.costs[i]:.5f}$
            """, help=f"{st.session_state.locale.sum_tokens}{sum(st.session_state.total_tokens)} | {st.session_state.locale.total_cost}{sum(st.session_state.costs):.5f}$")  # noqa: E501


def calc_total(prompt_tkns: int, compl_tkns: int, in_cost_pm: float, out_cost_pm: float) -> float:
    """
    Рассчитывает общую стоимость входных и выходных токенов с заданными тарифами.
    OpenAI pricing logic: https://openai.com/api/pricing/#language-models

    :param prompt_tkns: Количество входных токенов.
    :param compl_tkns: Количество выходных токенов.
    :param in_cost_pm: Стоимость за миллион входных токенов.
    :param out_cost_pm: Стоимость за миллион выходных токенов.
    :return: Общая стоимость токенов.
    """
    cost_per_input_token = in_cost_pm / 1_000_000
    cost_per_output_token = out_cost_pm / 1_000_000
    total_cost = (prompt_tkns * cost_per_input_token) + (compl_tkns * cost_per_output_token)
    return total_cost


def calc_cost(usage: CompletionUsage) -> None:
    total_tokens = usage.total_tokens
    st.session_state.user_tokens -= total_tokens
    debit_tokens(username=st.session_state.username, used_tokens=total_tokens)
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    st.session_state.total_tokens.append(total_tokens)
    match st.session_state.model:
        case AIModels.gpt4o.value:
            cost = calc_total(prompt_tkns=prompt_tokens, compl_tkns=completion_tokens,
                              in_cost_pm=2.5, out_cost_pm=10.)
        case AIModels.gpt_4o_mini.value:
            cost = calc_total(prompt_tkns=prompt_tokens, compl_tkns=completion_tokens,
                              in_cost_pm=.15, out_cost_pm=.6)
        case AIModels.o1_preview.value:
            cost = calc_total(prompt_tkns=prompt_tokens, compl_tkns=completion_tokens,
                              in_cost_pm=15., out_cost_pm=60.)
        case AIModels.o1.value:
            cost = calc_total(prompt_tkns=prompt_tokens, compl_tkns=completion_tokens,
                              in_cost_pm=15., out_cost_pm=60.)
        case AIModels.o1_mini.value:
            cost = calc_total(prompt_tkns=prompt_tokens, compl_tkns=completion_tokens,
                              in_cost_pm=1.1, out_cost_pm=4.4)
        case AIModels.o3_mini.value:
            cost = calc_total(prompt_tkns=prompt_tokens, compl_tkns=completion_tokens,
                              in_cost_pm=1.1, out_cost_pm=4.4)
        case _:
            cost = calc_total(prompt_tkns=prompt_tokens, compl_tkns=completion_tokens,
                              in_cost_pm=30., out_cost_pm=120.)
    st.session_state.costs.append(cost)


def show_gpt_conversation() -> None:
    try:
        completion = create_gpt_completion(st.session_state.model, st.session_state.messages)
        ai_content = completion.choices[0].message.content
        calc_cost(completion.usage)
        st.session_state.messages.append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_chat(ai_content)
            st.divider()
    # except InvalidRequestError as err:
    #     if err.code == "context_length_exceeded":
    #         st.session_state.messages.pop(1)
    #         if len(st.session_state.messages) == 1:
    #             st.session_state.user_text = ""
    #         show_conversation()
    #     else:
    #         st.error(err)
    #         st.stop()
    except (APIError, UnboundLocalError) as err:
        st.error(err)
        st.stop()


def append_user_message() -> None:
    st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})


def show_conversation() -> None:
    if st.session_state.messages:
        # st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
        append_user_message()
    else:
        if st.session_state.model not in [AIModels.o1.value, AIModels.o1_preview.value, AIModels.o1_mini.value]:
            ai_role = f"{st.session_state.locale.ai_role_prefix + ' ' if st.session_state.role else ''}" \
                      f"{st.session_state.role + '.' if st.session_state.role else ''}"
            st.session_state.messages = [
                {"role": "system", "content": ai_role + st.secrets.prompt.system},
            ]
        append_user_message()
    show_gpt_conversation()
