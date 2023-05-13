import datetime
import math

import pandas as pd
import sqlparse
import streamlit as st
from millify import millify

BLUE_COLOR = "#1c83e1"


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


def space(num_lines: int = 1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


def hbar():
    """Adds a horizontal bar"""
    st.write("---")


def subsubheader(*args):
    text = " · ".join(tuple(args))
    st.write(text)


def underline(text: str, color: str = BLUE_COLOR) -> str:
    """Underlines input text using HTML"""
    style = "font-size:18px; text-decoration-style: dotted; "
    style += "text-underline-offset: 5px; "
    style += f"text-decoration-color:{color};"
    return f"""<strong> <u style="{style}"> {text}</u> </strong>"""


def dataframe_with_podium(
    df: pd.DataFrame, sort_by: str = None
) -> pd.DataFrame:
    """Replaces dataframe indices 1, 2, 3 with medals 🥇, 🥈, 🥉"""

    if sort_by:
        # Sort dataframe and take top-10
        sorted_df = (
            df.sort_values(by=sort_by, ascending=False)
            .reset_index(drop=True)
            .head(10)
        )
    else:
        sorted_df = df.head(10).copy()

    # Replace index to highlight the podium (gold, metal, bronze)
    new_index = ["🥇", "🥈", "🥉"] + list(map(str, range(4, 11)))
    sorted_df.index = new_index[: len(sorted_df)]
    return sorted_df


def date_selector() -> tuple[datetime.date, datetime.date]:
    """Adds a date selector with a few different options."""

    DATE_RANGE_OPTIONS = [
        "Last 7 days",
        "Last 28 days",
        "Last 3 months",
        "Last 6 months",
        "Last 12 months",
        "All time",
        "Custom",
    ]

    if "date_range" in st.session_state:
        index = DATE_RANGE_OPTIONS.index(st.session_state.date_range)
    else:
        index = 0

    date_range = st.selectbox(
        "Date range",
        options=[
            "Last 7 days",
            "Last 28 days",
            "Last 3 months",
            "Last 6 months",
            "Last 12 months",
            "All time",
            "Custom",
        ],
        index=index,
        key="date_range",
    )

    if date_range != "Custom":
        date_to = datetime.date.today()
        if date_range == "Last 7 days":
            date_from = date_to - datetime.timedelta(days=7)
        elif date_range == "Last 28 days":
            date_from = date_to - datetime.timedelta(days=28)
        elif date_range == "Last 3 months":
            date_from = date_to - datetime.timedelta(weeks=12)
        elif date_range == "Last 6 months":
            date_from = date_to - datetime.timedelta(weeks=24)
        elif date_range == "Last 12 months":
            date_from = date_to - datetime.timedelta(days=365)
        else:
            date_from = datetime.date(year=2016, month=1, day=1)

    if "custom" in st.session_state:
        value = st.session_state.custom
    else:
        value = (
            date_to - datetime.timedelta(days=7),
            date_to,
        )

    if date_range == "Custom":
        date_from, date_to = st.date_input(
            "Choose start and end date",
            value=value,
            key="custom",
        )

    st.caption(f"Your selection is from **{date_from}** to **{date_to}**")

    return date_from, date_to


def pretty_print_credits(credits: float) -> str:
    return f"{millify(credits, 1)} Credits"


def pretty_print_bytes(size_bytes: int, binary: bool = False) -> str:
    basis = 1024 if binary else 1000
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, basis)))
    p = math.pow(basis, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i]) + " " * 8


def pretty_print_seconds(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    pretty_print = ""
    if hours:
        pretty_print += f"{hours} hr{'s' if hours > 1 else ''} "
    if minutes:
        pretty_print += f"{minutes} min{'s' if minutes > 1 else ''} "
    if seconds:
        pretty_print += f"{seconds} sec{'s' if seconds > 1 else ''}"
    return pretty_print


def pretty_print_sql_query(query: str) -> str:
    return sqlparse.format(
        query,
        reindent=True,
        keyword_case="upper",
    )


if __name__ == "__main__":
    pass
