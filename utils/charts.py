import altair as alt
import pandas as pd
import streamlit as st

from utils import gui

ALTAIR_AXIS_CONFIG = dict(
    gridColor="#e6eaf1",
    tickColor="#e6eaf1",
    domainColor="#e6eaf1",
    labelColor="#828797",
    titleFontWeight="bold",
)

ALTAIR_SCHEME = "blues"


@st.experimental_memo(ttl=60 * 60 * 12)
def get_bar_chart(
    df: pd.DataFrame,
    date_column: str,
    value_column: str,
    color: str = gui.BLUE_COLOR,
) -> alt.vegalite.v4.api.Chart:

    config = {
        "x": alt.X(f"yearmonthdate({date_column})", title="Day"),
        "y": alt.Y(f"sum({value_column})", title="Consumption"),
        "tooltip": (date_column, value_column),
    }

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(**config)
        .configure_mark(opacity=1, color=color)
        .configure_axis(**ALTAIR_AXIS_CONFIG)
        .interactive()
    )

    return chart


@st.experimental_memo(ttl=60 * 60 * 12)
def get_histogram_chart(
    df: pd.DataFrame,
    date_column: str,
) -> alt.vegalite.v4.api.Chart:

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(
                date_column,
                bin=alt.BinParams(
                    maxbins=100,
                ),
            ),
            y=alt.Y(
                "count()",
                title="Count of Records",
                scale=alt.Scale(type="symlog"),
            ),
            tooltip=[date_column, "count()"],
        )
        .configure_mark(
            color=gui.BLUE_COLOR,
        )
        .configure_axis(**ALTAIR_AXIS_CONFIG)
        .interactive()
    )

    return chart


@st.experimental_memo(ttl=60 * 60 * 12)
def get_scatter_chart(
    df: pd.DataFrame,
):
    chart = (
        alt.Chart(df)
        .mark_circle(
            size=200,
        )
        .encode(
            x=alt.X(
                "NUMBER_OF_QUERIES_LOG:Q",
                title="Number of queries (log scale)",
                scale=alt.Scale(
                    domain=[
                        df.NUMBER_OF_QUERIES_LOG.min() - 0.5,
                        df.NUMBER_OF_QUERIES_LOG.max() + 0.5,
                    ]
                ),
            ),
            y=alt.Y(
                "EXECUTION_MINUTES_LOG:Q",
                title="Execution minutes (log scale)",
                scale=alt.Scale(
                    domain=[
                        df.EXECUTION_MINUTES_LOG.min() - 0.5,
                        df.EXECUTION_MINUTES_LOG.max() + 0.5,
                    ]
                ),
            ),
            tooltip=[
                "QUERY_TEXT",
                "NUMBER_OF_QUERIES",
                "EXECUTION_MINUTES",
            ],
        )
        .configure_mark(opacity=0.7, color=gui.BLUE_COLOR)
        .configure_axis(**ALTAIR_AXIS_CONFIG)
        .interactive()
    )

    return chart


if __name__ == "__main__":
    pass
