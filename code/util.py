# Philip O'Sullivan
# Helper functions for CPD Lawsuit data processing

import re
import pandas as pd

WHITESPACE_PAT = re.compile(r"\s+")


def strip_and_trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Strips trailing and leading whitespace and removes an excess
    whitespace from dataframe column names and any string or object columns.

    Input:
        df: The dataframe to removes excess whitespace

    Returns:
        The same dataframe with the excess whitespace removed
    """
    # first fix column names
    df.columns = [WHITESPACE_PAT.sub(" ", col).strip() for col in df.columns]

    # now fix string columns
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.replace(WHITESPACE_PAT, " ")
            )

    return df
