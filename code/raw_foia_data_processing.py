""" This module has functions for transforming the raw data received from
the foia requests into to easy to work with csvs saved in the uncleaned csv
data folder. The only additional processing of the data is removing excess
whitespace and stripping leading and trailing whitespace from the values
in string columns and column names.
"""

# stdlib imports
import typing

# 3rd party imports
import pandas as pd

# repo specific imports
import directory_constants as DIR_C
import raw_data_constants as RAW_C
import util


def save_csv_formatted_foia_tort_payments_data() -> pd.DataFrame:
    """Loads the raw unmodified 2001 to 2007 tort payment data,
    changes it into a workable dataframe format, saves that as a csv
    then returns the dataframe as well
    """
    # skip the first 4 rows
    raw_foia_tort_payments_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_FOIA_DATA_DIR.joinpath(
            RAW_C.RAW_TORT_PAYMENTS_2001_TO_2007_FOIA_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_TORT_PAYMENTS_2001_TO_2007_FOIA_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
    )

    # fix any whitespace issues
    raw_foia_tort_payments_df = util.strip_and_trim_whitespace(
        raw_foia_tort_payments_df,
    )

    # do some value specific replacements
    payment_replace_dict = {"NONE": 0}

    raw_foia_tort_payments_df["PAYMENT AMOUNT ($)"].replace(
        to_replace=payment_replace_dict,
        inplace=True,
    )
    raw_foia_tort_payments_df["FEES & COSTS ($)"].replace(
        to_replace=payment_replace_dict,
        inplace=True,
    )
    # now convert to proper dtypes
    raw_foia_tort_payments_df["PAYMENT AMOUNT ($)"] = pd.to_numeric(
        raw_foia_tort_payments_df["PAYMENT AMOUNT ($)"]
    )
    raw_foia_tort_payments_df["FEES & COSTS ($)"] = pd.to_numeric(
        raw_foia_tort_payments_df["FEES & COSTS ($)"]
    )
    raw_foia_tort_payments_df["DATE TO COMPTROLLER"] = pd.to_datetime(
        raw_foia_tort_payments_df["DATE TO COMPTROLLER"]
    )

    # now save to csv
    util.save_df(
        df=raw_foia_tort_payments_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_TORT_PAYMENTS_2001_TO_2007_FOIA_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_FOIA_DATA_DIR,
    )
    return raw_foia_tort_payments_df


def save_csv_formatted_foia_cpd_payments_data() -> pd.DataFrame:
    """Loads the raw unmodified 2004 to 2018 cpd payment data,
    changes it into a workable dataframe format, saves that as a csv
    then returns the dataframe as well
    """
    # skip the first 4 rows and last 3 rows
    raw_foia_cpd_payments_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_FOIA_DATA_DIR.joinpath(
            RAW_C.RAW_CPD_PAYMENTS_2004_TO_2018_FOIA_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_CPD_PAYMENTS_2004_TO_2018_FOIA_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=3,
    )

    # fix any whitespace issues
    raw_foia_cpd_payments_df = util.strip_and_trim_whitespace(
        raw_foia_cpd_payments_df,
    )

    # now convert to proper dtypes
    raw_foia_cpd_payments_df["DATE TO COMPTROLLER"] = pd.to_datetime(
        raw_foia_cpd_payments_df["DATE TO COMPTROLLER"]
    )

    # now save to csv
    util.save_df(
        df=raw_foia_cpd_payments_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_CPD_PAYMENTS_2004_TO_2018_FOIA_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_FOIA_DATA_DIR,
    )
    return raw_foia_cpd_payments_df


def save_csv_formatted_foia_pending_suits_data() -> pd.DataFrame:
    """Loads the raw unmodified pending police lawsuits data,
    changes it into a workable dataframe format, saves that as a csv
    then returns the dataframe as well
    """
    # skip the first 4 rows
    raw_foia_pending_police_suits_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_FOIA_DATA_DIR.joinpath(
            RAW_C.RAW_PENDING_POLICE_SUITS_FOIA_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_PENDING_POLICE_SUITS_FOIA_DATA_EXCEL_SHEET,
        header=1,
        skipfooter=1,
    )

    # fix any whitespace issues
    raw_foia_pending_police_suits_df = util.strip_and_trim_whitespace(
        raw_foia_pending_police_suits_df,
    )

    # now save to csv
    util.save_df(
        df=raw_foia_pending_police_suits_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_PENDING_POLICE_SUITS_FOTA_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_FOIA_DATA_DIR,
    )
    return raw_foia_pending_police_suits_df


def format_multitable_df(
    unformatted_df: pd.DataFrame,
    header_row_value: str,
    subheading_col_name: str,
) -> pd.DataFrame:
    """Takes a dataframe which loaded an excel file with multiple
    subtables and combines all the subtables into one dataframe. The
    name of each subtable is put into the subheading_col_name value
    for a given subtable. Uses the header_row_value as the value for
    breaking up the dataframe into subtables

    Inputs:
        unformatted_df: The dataframe representing the entire sheet
        header_row_value: the value to be used to seperate the unformatted_df
                          into the multiple sub tables
        subheading_col_name: The name of the column to be added with the sub
                             table names as the value
    Output:
        The now properly formatted dataframe"""
    # drop all the empty rows and columns
    unformatted_df.dropna(how="all", axis=0, inplace=True)
    unformatted_df.dropna(how="all", axis=1, inplace=True)
    # reset the index
    unformatted_df.reset_index(drop=True, inplace=True)
    # make the column names predictable format
    unformatted_df.columns = [f"col{num}" for num in range(unformatted_df.shape[1])]
    # now find the columns which correspond to header rows
    header_rows_df = unformatted_df.query("col0 == @header_row_value")
    # assert all the header row cols have the same values
    assert header_rows_df.apply(lambda col: col.eq(col.iloc[0]).all()).all(), (
        "Not All of the columns identified as header rows"
        f"using {header_row_value} are equal!"
    )
    header_cols = header_rows_df.iloc[0].tolist()
    # Now we assume the sub table name is right before the header
    subtable_names_df = unformatted_df.loc[header_rows_df.index - 1]
    # check only first column has values
    assert subtable_names_df.iloc[:, 1:].isna().all().all(), (
        "The subtable name rows have at least one non-empty value"
        "in columns besides the first one"
    )
    assert subtable_names_df.iloc[:, 0].notna().all(), (
        "The subtable name rows have at least one empty value" "in the first column"
    )
    subtable_names = subtable_names_df["col0"].tolist()
    # now get the indices to slice up the unformatted dataframe
    # the lower bound is just the index of header row plus on
    subtable_df_lbs = (header_rows_df.index + 1).tolist()
    # the upper bound is gonna be subtable name rows minus one
    # but we ignore the first subtable name row and add the end of the dataframe
    subtable_df_ubs = subtable_names_df.index[1:] - 1
    subtable_df_ubs = subtable_df_ubs.tolist() + [unformatted_df.index[-1]]

    # make iterator of the subtable name and upper and lower bounds
    df_slice_iterator = zip(subtable_names, subtable_df_lbs, subtable_df_ubs)
    formatted_df = pd.DataFrame(columns=header_cols + [subheading_col_name])
    # now combine slices together
    for subtable_name, df_lb, df_ub in df_slice_iterator:
        # get the slice
        df_slice = unformatted_df.loc[df_lb:df_ub]
        # fix the name
        df_slice.columns = header_cols
        # add the subtable name
        df_slice[subheading_col_name] = subtable_name
        # now append
        formatted_df = formatted_df.append(df_slice, ignore_index=True)

    # sanity check that a header value is not in the formatted df
    assert not formatted_df.iloc[:, 0].isin([header_row_value]).any(), (
        f"There is still the header row value {header_row_value} in "
        "the finished formatting dataframe"
    )

    return formatted_df


def save_csv_formatted_quarterly_police_suit_disp_data() -> pd.DataFrame:
    """Loads the raw unmodified quarterly police lawsuits disposition data
    changes it into a workable dataframe format, saves that as a csv
    then returns the dataframe as well
    """
    # load the sheet which currently has multiple subtables in it
    unsplit_raw_foia_police_suits_disp_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_FOIA_DATA_DIR.joinpath(
            RAW_C.RAW_QUARTERLY_POLICE_SUIT_DISP_FOIA_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_QUARTERLY_POLICE_SUIT_DISP_FOIA_DATA_EXCEL_SHEET,
    )
    # properly format the subtables into one df
    raw_foia_police_suits_disp_df = format_multitable_df(
        unsplit_raw_foia_police_suits_disp_df,
        header_row_value="Docket Number",
        subheading_col_name="Client Department",
    )
    # strip the client department of the leading "Client Department:" value
    raw_foia_police_suits_disp_df["Client Department"] = (
        raw_foia_police_suits_disp_df["Client Department"]
        .str.lstrip("Client Department:")
        .str.strip()
    )

    # now save to csv
    util.save_df(
        df=raw_foia_police_suits_disp_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_QUARTERLY_POLICE_SUIT_DISP_FOIA_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_FOIA_DATA_DIR,
    )
    return raw_foia_police_suits_disp_df


def save_csv_formatted_matter_disp_report_data() -> typing.List[pd.DataFrame]:
    """Loads the raw unmodified matter disposition data
    changes it into a workable dataframe formats,
    saves each sheet as a csv then returns a list of the dataframes as well
    """
    output_list = []

    # sheet name, subheading col name and the output csv name
    sheet_save_list = [
        (
            RAW_C.RAW_QUARTERLY_MATTER_DISP_REPORT_BY_DIVISION_FOIA_DATA_EXCEL_SHEET,
            "Division",
            RAW_C.RAW_CSV_FORMATTED_MATTER_DISP_REPORT_BY_DIVISION_FOIA_DATA_CSV,
        ),
        (
            RAW_C.RAW_QUARTERLY_MATTER_DISP_REPORT_BY_DEPARTMENT_FOIA_DATA_EXCEL_SHEET,
            "Client Department",
            RAW_C.RAW_CSV_FORMATTED_MATTER_DISP_REPORT_BY_DEPARTMENT_FOIA_DATA_CSV,
        ),
        (
            RAW_C.RAW_QUARTERLY_MATTER_DISP_REPORT_BY_ASSIGNEE_FOIA_DATA_EXCEL_SHEET,
            "Main Assignee",
            RAW_C.RAW_CSV_FORMATTED_MATTER_DISP_REPORT_BY_ASSIGNEE_FOIA_DATA_CSV,
        ),
    ]

    for sheet_name, subtable_col_name, output_csv_name in sheet_save_list:

        unsplit_df = pd.read_excel(
            io=DIR_C.RAW_UNMODIFIED_FOIA_DATA_DIR.joinpath(
                RAW_C.RAW_QUARTERLY_MATTER_DISP_REPORT_FOIA_DATA_EXCEL_FILE
            ),
            sheet_name=sheet_name,
        )
        # properly format the subtables into one df
        formatted_df = format_multitable_df(
            unsplit_df,
            header_row_value="Docket Number",
            subheading_col_name=subtable_col_name,
        )

        # strip the client department of the leading "Division:" value
        formatted_df[subtable_col_name] = (
            formatted_df[subtable_col_name]
            .str.lstrip(subtable_col_name + ":")
            .str.strip()
        )
        output_list.append(formatted_df)

        # now save to csv
        util.save_df(
            df=formatted_df,
            file_name=output_csv_name,
            save_dir=DIR_C.RAW_CSV_FORMATTED_FOIA_DATA_DIR,
        )

    return output_list


def raw_foia_data_processing_main() -> None:
    """Main function for the raw foia data processing module which
    processes all the unmodified raw data files and saves them in
    a csv formatted version"""
    save_csv_formatted_foia_tort_payments_data()
    save_csv_formatted_foia_cpd_payments_data()
    save_csv_formatted_foia_pending_suits_data()
    save_csv_formatted_quarterly_police_suit_disp_data()
    save_csv_formatted_matter_disp_report_data()


if __name__ == "__main__":
    raw_foia_data_processing_main()
