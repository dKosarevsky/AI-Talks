# mypy: ignore-errors

import streamlit as st
from bokeh.models import CustomJS
from bokeh.models.widgets import Button
from streamlit_bokeh_events import streamlit_bokeh_events

REC_GIF = "ai_talks/assets/icons/rec_on.gif"


def get_js_code(lang: str) -> str:
    return """
        var value = "";
        var rand = 0;
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
    """ + f"recognition.lang = '{lang}';" + """
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'start'}));

        recognition.onspeechstart = function () {
            document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'running'}));
        }
        recognition.onsoundend = function () {
            document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
        }
        recognition.onresult = function (e) {
            var value2 = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                    rand = Math.random();

                } else {
                    value2 += e.results[i][0].transcript;
                }
            }
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: {t:value, s:rand}}));
            document.dispatchEvent(new CustomEvent("GET_INTRM", {detail: value2}));

        }
        recognition.onerror = function(e) {
            document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
        }
        recognition.start();
    """


def show_speak_btn() -> Button:
    stt_button = Button(label=st.session_state.locale.speak_btn, button_type="success", width=100)
    stt_button.js_on_event("button_click", CustomJS(code=get_js_code(st.session_state.locale.lang_code)))
    return stt_button


def get_bokeh_result() -> dict:
    stt_button = show_speak_btn()
    return streamlit_bokeh_events(
        bokeh_plot=stt_button,
        events="GET_TEXT,GET_ONREC,GET_INTRM",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0,
    )


def show_voice_input() -> None:
    if "input" not in st.session_state:
        st.session_state.input = {"text": "", "session": 0}
    result = get_bokeh_result()
    tr = st.empty()
    tr.code(st.session_state.input["text"])
    if result:
        if "GET_TEXT" in result and (
                result.get("GET_TEXT")["t"] != "" and result.get("GET_TEXT")["s"] != st.session_state.input["session"]):
            st.session_state.input["text"] = result.get("GET_TEXT")["t"]  # type: ignore
            tr.code(st.session_state.input["text"])
            st.session_state.input["session"] = result.get("GET_TEXT")["s"]
        if "GET_INTRM" in result and result.get("GET_INTRM") != "":
            tr.code(st.session_state.input["text"] + " " + result.get("GET_INTRM"))
        if "GET_ONREC" in result:
            if result.get("GET_ONREC") == "start":
                st.image(REC_GIF)
                st.session_state.input["text"] = ""
            elif result.get("GET_ONREC") == "running":
                st.image(REC_GIF)
            elif result.get("GET_ONREC") == "stop" and st.session_state.input["text"] != "":
                st.session_state.user_text = st.session_state.input["text"]
                st.session_state.input["text"] = ""
