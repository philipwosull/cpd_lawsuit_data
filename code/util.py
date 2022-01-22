# Philip O'Sullivan
# Helper functions for CPD Lawsuit data processing

# stdlib imports
import re
import typing
import pathlib

# 3rd party imports
import pandas as pd


def load_df(
    file_name: str,
    save_dir: pathlib.Path,
    sheet_name: str = "",
    datetime_converserions: typing.Tuple[str, str] = {},
) -> pd.DataFrame:
    """
    Takes a filename and a directory then loads a dataframe from that
    file and returns it

    Inputs:
        file_name(string): the name of the file the df will be loaded from
        save_dir(pathlib path): the directory the file is in
        sheet_name(str): optional name of sheet if excel
        datetime_converserions(Dict[str, str]): An optional type of
        column name, datetime format to convert

    Output:
        a dataframe loaded from the file
    """
    # load depending on file ending
    if file_name.endswith(".csv"):
        df = pd.read_csv(save_dir / file_name)
    elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        # assert they didn't forget a sheet
        assert sheet_name != "", f"No sheet included with {file_name}"
        # load frame
        df = pd.read_excel(save_dir / file_name, sheet_name=sheet_name)

    else:
        raise NotImplementedError(
            "This function does not currently support the file extension "
            + f"for {file_name}"
        )

    # now attempt to get a good dtype
    df = df.apply(
        pd.to_numeric,
        errors="ignore",
        downcast="unsigned",
    ).convert_dtypes()

    # now do date time conversions
    for col, datetime_format in datetime_converserions:
        df[col] = pd.to_datetime(df[col], format=datetime_format)

    return df


def save_df(df: pd.DataFrame, file_name: str, save_dir: pathlib.Path) -> None:
    """
    Takes a dataframe, a filename, and a directory. The dataframe will
    be saved with the file name in the given directory

    Inputs:
        df(pandas dataframe): dataframe to save
        file_name(string): the name of the file the df will be saved as
        save_dir(pathlib path): the directory the file should be saved in

    Output:
        nothing
    """

    # now save the name
    if file_name.endswith(".csv"):
        df.to_csv(save_dir / file_name, index=False)
    else:
        raise NotImplementedError(
            "This function does not currently support the file extension "
            + f"for {file_name}"
        )


def strip_and_trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Strips trailing and leading whitespace and removes an excess
    whitespace from dataframe column names and any string or object columns.

    Input:
        df: The dataframe to removes excess whitespace

    Returns:
        The same dataframe with the excess whitespace removed
    """
    # define whitespace pattern
    whitespace_pat = re.compile(r"\s+")
    # first fix column names
    df.columns = [whitespace_pat.sub(" ", col).strip() for col in df.columns]

    # now fix string columns
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.replace(whitespace_pat, " ")
            )

    return df
