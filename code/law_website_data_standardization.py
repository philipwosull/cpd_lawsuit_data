""" This module contains code to standarize and clean the csv formatted raw
law department website data accross all years. Specifically it standardizes
- Column names
- Case Numbers
- Payment amount and fee columns to numeric

The standardized version of the data can be appended together accross any
year. Note that this data is all lawsuits filed against the City, not just
those involving the Chicago police.
"""
# 3rd party imports
import pandas as pd

# repo specific imports
import raw_data_constants as RAW_C
import directory_constants as DIR_C
import data_standardization_constants as STAN_C
import case_number_standardization as case_num_parsing
import util


def clean_and_standardize_all_data() -> None:
    """Cleans, standardizes, and saves Law Website data from each year.

    Cleans, standardizes and saves the Law Website data for each year.
    It also saves a single file with all the years combined into one."""
    # list of tuples with (raw_csv, output_csv)
    processing_list = [
        (
            RAW_C.RAW_CSV_FORMATTED_2008_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2008_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2009_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2009_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2010_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2010_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2011_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2011_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2012_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2012_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2013_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2013_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2014_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2014_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2015_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2015_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2016_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2016_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2017_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2017_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2018_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2018_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2019_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2019_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2020_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2020_LAW_WEBSITE_DATA_CSV,
        ),
        (
            RAW_C.RAW_CSV_FORMATTED_2021_LAW_WEBSITE_DATA_CSV,
            STAN_C.STANDARDIZED_2021_LAW_WEBSITE_DATA_CSV,
        ),
    ]

    rename_dict = STAN_C.LAW_WEBSITE_DATA_COL_STANDARDIZATION_RENAME_DICT
    output_dfs = []

    doc_yr = 2008
    for raw_csv, output_csv in processing_list:
        raw_df = util.load_df(
            file_name=raw_csv,
            save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
        )
        assert raw_df.columns.isin(
            rename_dict.keys()
        ).all(), f"Not all keys in {raw_csv} are in the rename dict!"
        # rename
        standardized_df = raw_df.rename(columns=rename_dict)
        # standardize case number and extract relevant info
        standardized_df = case_num_parsing.standardize_case_num_info(standardized_df)
        # remove 0931 from department name (included one year for some reason)
        standardized_df[STAN_C.CITY_DEPARTMENT_INVOLVED_COL] = standardized_df[
            STAN_C.CITY_DEPARTMENT_INVOLVED_COL
        ].str.rstrip(" 0931")
        # if any numeric columns not numeric then fix them
        already_numeric_cols = standardized_df.select_dtypes("number").columns
        # remove and dollar signs or commas from payment column
        for money_col in [STAN_C.PAYMENT_AMOUNT_COL, STAN_C.FEES_AND_COSTS_COL]:
            # skip if already numberic
            if money_col in already_numeric_cols:
                continue

            standardized_df[money_col] = pd.to_numeric(
                standardized_df[money_col].str.replace(
                    pat=r"[\,\$\s]+", repl="", regex=True
                )
            )
        # add data source
        standardized_df[STAN_C.DATA_SOURCE_COL] = f"law_dept_website_{doc_yr}"
        doc_yr += 1
        # save output
        util.save_df(
            df=standardized_df,
            file_name=output_csv,
            save_dir=DIR_C.CLEANED_AND_STANDARDIZED_LAW_WEBSITE_DATA_DIR,
        )
        output_dfs.append(standardized_df)

    all_yrs_output_df = pd.concat(output_dfs)
    util.save_df(
        df=all_yrs_output_df,
        file_name=STAN_C.STANDARDIZED_ALL_YEARS_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.CLEANED_AND_STANDARDIZED_LAW_WEBSITE_DATA_DIR,
    )


if __name__ == "__main__":
    clean_and_standardize_all_data()
