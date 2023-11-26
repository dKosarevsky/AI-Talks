import logging
import streamlit as st

from .api_utils import get_api_client


@st.cache_data()
def gen_dalle_img(ai_model: str = "dall-e-3", prompt: str = "A photograph of a white Siamese cat.") -> None:
    client = get_api_client()
    logging.info(f"{prompt=}")
    response = client.images.generate(
        model=ai_model,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    st.image(response.data[0].url)
    # DALL·E 3
    # Standard	1024×1024	$0.040 / image
    # Standard	1024×1792, 1792×1024	$0.080 / image
