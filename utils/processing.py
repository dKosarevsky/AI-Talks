import numpy as np
import pandas as pd
import streamlit as st


@st.experimental_memo
def resample_by_day(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """Resample a dataframe's date_column by day, summing values."""
    return (
        df.set_index(date_column).resample("1D").sum().reset_index(date_column)
    )


@st.experimental_memo
def resample_date_period(
    df: pd.DataFrame, date_from: str, date_to: str, value_column: str
) -> pd.DataFrame:
    """Resample a dataframe to make sure there are values in value_column
    for the full date period from date_from to date_to."""

    empty_df = pd.DataFrame()
    empty_df["START_TIME"] = pd.date_range(date_from, date_to, freq="H")
    empty_df[value_column] = 0
    return empty_df.append(
        df,
        ignore_index=True,
    )


@st.experimental_memo
def apply_log1p(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Apply log1p on input columns and store into new columns in input df
    with suffix _LOG."""
    log_columns = [f"{column}_LOG" for column in columns]
    df[log_columns] = df[columns].apply(np.log1p)
    return df


if __name__ == "__main__":
    pass
