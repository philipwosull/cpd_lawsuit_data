""" Module for standardizing and extracting relevant information from case numbers.

Module with functions and constants for standardizing case numbers and
extracting relevant information (filing year, case type, etc.) from case
number.
"""

# stdlib imports
import re

# 3rd party imports
import pandas as pd

# repo specific
import data_standardization_constants as STAN_C


# pattern to match federal civil case docket
FEDERAL_CIVIL_CASE_PAT = re.compile(
    rf"""\s* # leading whitespace to ignore
    (?P<{STAN_C.YEAR_FILED_COL}>\d{{2}}) # this is the year the case was filed
    \s*[-]* # any potential whitespace or a dash
    C[V]? # the C or CV to denote federal district court
    \s*[-]* # any potential whitespace or a dash
    (?P<{STAN_C.YEAR_CASE_NUMBER_COL}>\d+) # the year specific case number
    \s* # any trailing whitespace which can be ignored
    """,
    flags=re.VERBOSE | re.IGNORECASE,
)


def get_fed_civil_canonical_case_num(match_ob: re.Match) -> str:
    """Takes match of federal civil case number string and returns canonical form.

    Parameters
    ----------
    match_ob
        A re match with the federal civil case number pattern match.

    Returns
    -------
    str
        The canonical (standardized) form of a federal civil case number.
        This is YYYYFCV<filing number>. (FCV stands for federal civil)
    """
    match_dict = match_ob.groupdict()
    filing_year = match_dict[STAN_C.YEAR_FILED_COL]
    # either add 19 or 20 in front depending on year
    if int(filing_year) <= 30:
        filing_year = "20" + filing_year
    else:
        filing_year = "19" + filing_year
    filing_num = match_dict[STAN_C.YEAR_CASE_NUMBER_COL]
    return f"{filing_year}FCV{filing_num}"


# pattern to match Cook County Court Law division case
LAW_DIV_CASE_PAT = re.compile(
    rf"""\s* # leading whitespace to ignore
    (?P<{STAN_C.YEAR_FILED_COL}>\d{{2}}) # this is the year the case was filed
    \s*[-]* # any potential whitespace or a dash
    L # the L denotes law division case
    \s*[-]* # any potential whitespace or a dash
    (?P<{STAN_C.YEAR_CASE_NUMBER_COL}>\d+) # the year specific case number
    \s* # any trailing whitespace which can be ignored
    """,
    flags=re.VERBOSE | re.IGNORECASE,
)


def get_law_div_canonical_case_num(match_ob: re.Match) -> str:
    """Takes match of law division case number string and returns canonical form.

    Parameters
    ----------
    match_ob
        A re match with the law division case number pattern match.

    Returns
    -------
    str
        The canonical (standardized) form of a law division case number.
        This is YYYYCKL<filing number>. (CKL stands for Cook County Law)
    """
    match_dict = match_ob.groupdict()
    filing_year = match_dict[STAN_C.YEAR_FILED_COL]
    # either add 19 or 20 in front depending on year
    if int(filing_year) <= 30:
        filing_year = "20" + filing_year
    else:
        filing_year = "19" + filing_year
    filing_num = match_dict[STAN_C.YEAR_CASE_NUMBER_COL]
    return f"{filing_year}CKL{filing_num}"


# pattern to match Cook County Court Municipal division cases
MUNICIPAL_DIV_CASE_PAT = re.compile(
    rf"""\s* # leading whitespace to ignore
    (?P<{STAN_C.YEAR_FILED_COL}>\d{{2}}) # this is the year the case was filed
    \s*[-]* # any potential whitespace or a dash
    M[1]? # the M or M1 denotes municipal division case
    \s*[-]* # any potential whitespace or a dash
    (?P<{STAN_C.YEAR_CASE_NUMBER_COL}>\d+) # the year specific case number
    \s* # any trailing whitespace which can be ignored
    """,
    flags=re.VERBOSE | re.IGNORECASE,
)


def get_muni_div_canonical_case_num(match_ob: re.Match) -> str:
    """Takes match of municipal division case number string and returns canonical form.

    Parameters
    ----------
    match_ob
        A re match with the municipal division case number pattern match.

    Returns
    -------
    str
        The canonical (standardized) form of a municipal division case number.
        This is YYYYCKM<filing number>. (CKM stands for Cook County Municipal)
    """
    match_dict = match_ob.groupdict()
    filing_year = match_dict[STAN_C.YEAR_FILED_COL]
    # either add 19 or 20 in front depending on year
    if int(filing_year) <= 30:
        filing_year = "20" + filing_year
    else:
        filing_year = "19" + filing_year
    filing_num = match_dict[STAN_C.YEAR_CASE_NUMBER_COL]
    return f"{filing_year}CKM{filing_num}"


# pattern to match administrative
ADMINISTRATIVE_FILING_PAT = re.compile(
    rf"""\s* # leading whitespace to ignore
    182-A # all administrative cases start with this prefix
    (?P<{STAN_C.YEAR_CASE_NUMBER_COL}>\d+[-]?\d+) # the actual case number
    \s* # any trailing whitespace which can be ignored
    """,
    flags=re.VERBOSE | re.IGNORECASE,
)


def get_admin_claim_canonical_case_num(match_ob: re.Match) -> str:
    """Takes match of city admin claim case number string and returns canonical form.

    Parameters
    ----------
    match_ob
        A re match with the city admin claim case number pattern match.

    Returns
    -------
    str
        The canonical (standardized) form of a municipal division case number.
        This is ADMINC182-A<filing number>. (ADMINC stands for admin claim)
    """
    filing_num = match_ob.groupdict()[STAN_C.YEAR_CASE_NUMBER_COL]
    return f"ADMINC182-A{filing_num}"


def standardize_case_num_info(df: pd.DataFrame) -> pd.DataFrame:
    """Gets canonical form of case number and other relevant info.

    Takes a dataframe with a case number column and, using regex,
    parses the case numbers to get a canonical (i.e. standardized) version
    of the case number and extracts filing year/number if relevant.

    Parameters
    ----------
    df
        Dataframe containing a case number column to be standardized.

    Returns
    -------
    pd.DataFrame
        The same dataframe with the case number now in a canonical form along
        with case filing year/number extracted if relevant.
    """
    # list of tuples of (case pattern, case type, gov level, canonical_func)
    parsing_list = [
        (
            FEDERAL_CIVIL_CASE_PAT,
            STAN_C.FEDERAL_CIVIL_CASE_TYPE,
            STAN_C.FEDERAL_LEVEL_TYPE,
            get_fed_civil_canonical_case_num,
        ),
        (
            LAW_DIV_CASE_PAT,
            STAN_C.LAW_DIV_CASE_TYPE,
            STAN_C.MUNICIPAL_LEVEL_TYPE,
            get_law_div_canonical_case_num,
        ),
        (
            MUNICIPAL_DIV_CASE_PAT,
            STAN_C.MUNICIPAL_DIV_CASE_TYPE,
            STAN_C.MUNICIPAL_LEVEL_TYPE,
            get_muni_div_canonical_case_num,
        ),
        (
            ADMINISTRATIVE_FILING_PAT,
            STAN_C.CITY_ADMIN_CLAIM_CASE_TYPE,
            STAN_C.CITY_LEVEL_TYPE,
            get_admin_claim_canonical_case_num,
        ),
    ]
    # insert the new columns all empty for now after case number
    insert_index = df.columns.get_loc(STAN_C.RAW_CASE_NUM_COL) + 1
    df.insert(insert_index, STAN_C.CASE_GOV_LEVEL_COL, pd.Series(dtype="string"))
    df.insert(insert_index, STAN_C.CASE_TYPE_COL, pd.Series(dtype="string"))
    df.insert(insert_index, STAN_C.YEAR_CASE_NUMBER_COL, pd.Series(dtype="string"))
    df.insert(insert_index, STAN_C.YEAR_FILED_COL, pd.Series(dtype="string"))
    df.insert(insert_index, STAN_C.CANONICAL_CASE_NUM_COL, pd.Series(dtype="string"))

    # keep a list for checking no case numbers matches more than one pattern
    match_masks = []

    for pat, case_type, gov_level, canonical_func in parsing_list:
        # extract groups if any
        extracted_cols_df = df[STAN_C.RAW_CASE_NUM_COL].str.extract(pat)
        # get the rows that match
        match_mask = extracted_cols_df.notna().any(axis=1)

        # skip if no matches, currently only seems to happen for city admin
        # claims in the later 2010s onward. Probably changed their system.
        if not match_mask.any():
            print(f"No matches for {case_type}, had to skip!")
            continue

        # get canonical case number
        df.loc[match_mask, STAN_C.CANONICAL_CASE_NUM_COL] = df[match_mask][
            STAN_C.RAW_CASE_NUM_COL
        ].str.replace(pat=pat, repl=canonical_func, regex=True)

        # set the case type and gov level for those rows
        df.loc[match_mask, STAN_C.CASE_TYPE_COL] = case_type
        df.loc[match_mask, STAN_C.CASE_GOV_LEVEL_COL] = gov_level
        # extract year filed and filing number
        df.loc[
            match_mask,
            [STAN_C.YEAR_FILED_COL, STAN_C.YEAR_CASE_NUMBER_COL],
        ] = extracted_cols_df[match_mask]
        # for year filed turn into full year
        df.loc[
            match_mask & df[STAN_C.YEAR_FILED_COL].notna(), STAN_C.YEAR_FILED_COL
        ] = df.loc[
            match_mask & df[STAN_C.YEAR_FILED_COL].notna(), STAN_C.YEAR_FILED_COL
        ].apply(
            lambda yr: f"20{yr}" if int(yr) <= 30 else f"19{yr}"
        )

        match_masks.append(match_mask)

    # now check each row had at most one match
    row_matches = pd.concat(match_masks, axis=1)
    assert row_matches.sum(axis=1).le(1).all(), (
        f"{row_matches.sum(axis=1).sum()} rows match more than one "
        "case number pattern!"
    )

    # fill na values
    df[STAN_C.CASE_TYPE_COL].fillna(STAN_C.OTHER_CASE_TYPE, inplace=True)
    df[STAN_C.CASE_GOV_LEVEL_COL].fillna(STAN_C.OTHER_LEVEL, inplace=True)
    # for non matching case numbers just remove all the whitespace
    df.loc[~row_matches.any(axis=1), STAN_C.CANONICAL_CASE_NUM_COL] = df.loc[
        ~row_matches.any(axis=1), STAN_C.RAW_CASE_NUM_COL
    ].str.replace(pat=re.compile(r"\s+"), repl="")

    return df
