import logging
import streamlit as st
from openai import BadRequestError

from .api_utils import get_api_client
from ..back import debit_tokens
from ..constants import QualityDALLE, SizeDALLE


@st.cache_data()
def gen_dalle_img(ai_model: str, prompt: str, size: str, quality: str, style: str) -> None:
    """Generate DALL·E 3 image
    https://platform.openai.com/docs/guides/images/introduction

    Standard	1024×1024             $0.040 / image
    Standard	1024×1792, 1792×1024  $0.080 / image
    HD	        1024×1024             $0.080 / image
    HD	        1024×1792, 1792×1024  $0.120 / image
    """
    if not prompt:
        st.warning("Empty Prompt!")
        st.stop()
    logging.info(f"{prompt=}")
    client = get_api_client()
    try:
        response = client.images.generate(
            model=ai_model,
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1,
        )
        st.markdown(f"{st.session_state.locale.dalle_revised_prompt_placeholder}{response.data[0].revised_prompt}")
        calc_dalle_used_tokens(size=size, quality=quality)
        st.image(response.data[0].url)
    except BadRequestError as err:
        st.error(err)


def calc_dalle_used_tokens(size: str, quality: str) -> None:
    match (quality, size):
        case (QualityDALLE.standard.value, SizeDALLE.size_1024x1024.value):
            used_tokens = 1200
        case (QualityDALLE.standard.value, SizeDALLE.size_1024x1792.value):
            used_tokens = 2400
        case (QualityDALLE.standard.value, SizeDALLE.size_1792x1024.value):
            used_tokens = 2400
        case (QualityDALLE.hd.value, SizeDALLE.size_1024x1024.value):
            used_tokens = 2400
        case (QualityDALLE.hd.value, SizeDALLE.size_1024x1792.value):
            used_tokens = 3600
        case (QualityDALLE.hd.value, SizeDALLE.size_1792x1024.value):
            used_tokens = 3600
        case _:
            used_tokens = 3600
    st.session_state.user_tokens -= used_tokens
    debit_tokens(username=st.session_state.username, used_tokens=used_tokens)
