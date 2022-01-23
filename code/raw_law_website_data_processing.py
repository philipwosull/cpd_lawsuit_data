# Philip O'Sullivan
""" This module has functions for transforming the raw annual lawsuit data
from the Law Department website (for 2008 to 2021) into to easy to work with
csvs saved in the uncleaned csv data folder. The only additional processing of
the data is removing excess whitespace and stripping leading and
trailing whitespace from the values in string columns and column names.
"""

# stdlib imports
import re
import collections

# 3rd party imports
import pandas as pd
import numpy as np
import camelot

# Repo specific
import raw_data_constants as RAW_C
import directory_constants as DIR_C
import util

# pattern for splitting fee and primary cause columns in 2008 and 2009
FEE_AND_PRIM_CASE_PAT = re.compile(r"\s*([,\d]+)\s*(.+)", flags=re.DOTALL)


def process_2008_law_website_data() -> pd.DataFrame:
    """Loads the raw 2008 settlement data from the law department website,
    converts it from pdf to a pandas dataframe, then saves it as a csv
    and returns the dataframe from the function
    """
    # get the path to the pdf
    raw_2008_pdf_path = DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
        RAW_C.RAW_2008_LAW_WEBSITE_DATA_PDF
    )
    # use camelot to convert the first 55 pages tables to dataframes
    tables = camelot.read_pdf(filepath=str(raw_2008_pdf_path), pages="1-55")
    first_page_header_string = (
        "PAYMENT \nFEES & \nCITY \nDATE \nAMOUNT \nCOSTS "
        "\nDEPARTMENT \nTO \nCASE # \nPAYEE \n($) \n($) \nPRIMARY CAUSE "
        "\nINVOLVED \nDISPOSITION \nCOMPTROLLER \nTORT"
    )
    # expected headers for all pages besides the first
    non_first_page_header_string = (
        "PAYMENT \nFEES & \nCITY \nDATE "
        "\nDEPARTMENT \nTO \nAMOUNT \nCOSTS \nINVOLVED \nDISPOSITION "
        "\nCOMPTROLLER \nCASE # \nPAYEE \n($) \n($) \nPRIMARY CAUSE"
    )
    # define the dtypes
    raw_2008_df_col_types = collections.OrderedDict(
        {
            "CASE #": str,
            "PAYEE": str,
            "PAYMENT AMOUNT($)": int,
            "FEES & COSTS($)": int,
            "PRIMARY CAUSE": str,
            "CITY DEPARTMENT INVOLVED": str,
            "DISPOSITION": str,
            "DATE TO COMPTROLLER": np.datetime64,
            "Tort Status": str,
            "pdf_page_num": int,
        }
    )
    raw_2008_df_cols = raw_2008_df_col_types.keys()

    # special replacements for the payment amount column
    payment_amount_replacements = {
        "A \n5,694": "5694",
        "S \n76,000": "76000",
        "(181)": "-181",
        "(2,374)": "-2374",
    }
    # create an empty dataframe
    raw_2008_df = pd.DataFrame(columns=raw_2008_df_cols)
    last_page = 55

    # append all the pages' tables together
    for index, table in enumerate(tables):
        page_num = index + 1
        # extract the table as a dataframe
        table_df = table.df

        # check every cell besides first one on first row is empty string
        assert table_df.iloc[0].iloc[1:].eq("").all()
        if page_num == 1:
            assert table_df.iloc[0][0] == first_page_header_string
        else:
            assert table_df.iloc[0][0] == non_first_page_header_string
        # now drop that first row
        table_df = table_df.drop(index=[0])

        # special shape on first pass
        # check the first row is just the header values in one cell
        if page_num == 1:
            assert table_df.shape == (44, 8)
            table_df["Tort Status"] = "TORT"
        # special rules for last page
        elif page_num == last_page:
            assert table_df.shape == (47, 8)
            # make everything after 37 non tort and everything before tort
            assert table_df[0].loc[37] == "NON-TORT"
            assert table_df.loc[47][0] == (
                "TOTAL JUDGMENT/VERDICTS & "
                "SETTLEMENTS \n129,670,864 \nTOTAL FEES AND COSTS \n6,903,180"
            )
            table_df.loc[:37, "Tort Status"] = "TORT"
            table_df.loc[37:, "Tort Status"] = "NON-TORT"
            # drop the non tort lable row and the last one
            table_df = table_df.drop(index=[37, 47])
        else:
            # special shape on some pages with 50 rows instead of 51
            if page_num in [12, 41, 47, 49, 51, 53]:
                assert table_df.shape == (49, 8)
            else:
                assert table_df.shape == (50, 8)
            table_df["Tort Status"] = "TORT"

        table_df["pdf_page_num"] = page_num

        # rename the column
        table_df.columns = raw_2008_df_cols
        # fix the issue with the fees and primary cause column getting jumbled
        table_df[["FEES & COSTS($)", "PRIMARY CAUSE"]] = (
            table_df["FEES & COSTS($)"]
            .str.cat(table_df["PRIMARY CAUSE"])
            .str.extract(FEE_AND_PRIM_CASE_PAT)
        )

        # do special replacements and convert the numerical columns
        table_df["FEES & COSTS($)"] = (
            table_df["FEES & COSTS($)"].str.replace(",", "").astype(int)
        )
        table_df["PAYMENT AMOUNT($)"].replace(
            payment_amount_replacements,
            inplace=True,
        )
        table_df["PAYMENT AMOUNT($)"] = (
            table_df["PAYMENT AMOUNT($)"].str.replace(",", "").astype(int)
        )

        # now append
        raw_2008_df = raw_2008_df.append(table_df, ignore_index=True)

    # convert to datetime
    raw_2008_df["DATE TO COMPTROLLER"] = pd.to_datetime(
        raw_2008_df["DATE TO COMPTROLLER"]
    )
    # fix dtypes
    raw_2008_df = raw_2008_df.astype(raw_2008_df_col_types)
    # do whitespace fixing
    raw_2008_df = util.strip_and_trim_whitespace(raw_2008_df)

    # save to csv
    util.save_df(
        df=raw_2008_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2008_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2008_df


def process_2009_law_website_data() -> pd.DataFrame:
    """Loads the raw 2009 settlement data from the law department website,
    converts it from pdf to a pandas dataframe, then saves it as a csv
    and returns the dataframe
    """
    # get the path to the pdf
    raw_2009_pdf_path = DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
        RAW_C.RAW_2009_LAW_WEBSITE_DATA_PDF
    )
    # use camelot to convert the first 21 pages tables to dataframes
    tables = camelot.read_pdf(filepath=str(raw_2009_pdf_path), pages="1-21")
    first_page_header_string = (
        "PAYMENT \nFEES & \nCITY \nDATE \nAMOUNT \nCOSTS "
        "\nDEPARTMENT \nTO \nCASE # \nPAYEE \n($) \n($) \nPRIMARY CAUSE "
        "\nINVOLVED \nDISPOSITION \nCOMPTROLLER \nTORT"
    )

    # the first pages table has less rows than normal
    raw_2009_df_col_types = collections.OrderedDict(
        {
            "CASE #": str,
            "PAYEE": str,
            "PAYMENT AMOUNT($)": int,
            "FEES & COSTS($)": int,
            "PRIMARY CAUSE": str,
            "CITY DEPARTMENT INVOLVED": str,
            "DISPOSITION": str,
            "DATE TO COMPTROLLER": np.datetime64,
            "Tort Status": str,
            "pdf_page_num": int,
        }
    )
    raw_2009_df_cols = raw_2009_df_col_types.keys()

    # special replacements for the payment amount column
    payment_amount_replacements = {
        "(2,144)": "-2144",
        "(14,405)": "-14405",
        "(1,340)": "-1340",
        "(1,000)": "-1000",
        "(1,352)": "-1352",
        "(1,353)": "-1353",
        "(500)": "-500",
        "(1,175)": "-1175",
        "($550.23)": "550.23",
        "$620.00": "620",
        "$223.83": "223.83",
        "$450.00": "450",
        "$2,499.15": "2,499.15",
    }

    last_page = 21
    raw_2009_df = pd.DataFrame(columns=raw_2009_df_cols)

    # append all the pages' tables together
    for index, table in enumerate(tables):
        page_num = index + 1
        # extract the table as a dataframe
        table_df = table.df.copy()

        # special shape on first pass
        # check the first row is just the header values in one cell
        if page_num == 1:
            # check every cell besides first one on first row is empty string
            assert table_df.iloc[0].iloc[1:].eq("").all()
            assert table_df.iloc[0][0] == first_page_header_string
            # now drop that first row
            table_df = table_df.drop(index=[0])
            assert table_df.shape == (46, 8)
            table_df["Tort Status"] = "TORT"
        # special rule for page 20 where there is a split of tort and non-tort
        elif page_num == 20:
            assert table_df.loc[25].iloc[0] == "NON-TORT"
            table_df = table_df.drop(index=[25])
            assert table_df.shape == (54, 8)
            table_df.loc[:25, "Tort Status"] = "TORT"
            table_df.loc[25:, "Tort Status"] = "NON-TORT"
        # special rules for last page
        elif page_num == last_page:
            assert table_df.shape == (47, 8)
            # check the last row is the sums
            assert table_df.loc[46][0] == (
                "TOTAL JUDGMENT/VERDICTS & "
                "SETTLEMENTS \n51,155,053 \nTOTAL FEES AND COSTS \n7,660,924 "
                "\nTOTAL JUDGMENT/VERDICTS, SETTLEMENTS, FEES AND COSTS \n58,815,977"
            )
            table_df["Tort Status"] = "NON-TORT"
            # drop the non tort lable row and the last one
            table_df = table_df.drop(index=[46])
        else:
            assert table_df.shape == (55, 8)
            table_df["Tort Status"] = "TORT"
        # add a page number
        table_df["pdf_page_num"] = page_num

        # rename the column
        table_df.columns = raw_2009_df_cols

        # specific value rename since the number was cutoff
        if page_num == 9:
            table_df.loc[13, "PAYMENT AMOUNT($)"] = "1395000"

        # fix the issue with the fees and primary cause column getting jumbled
        assert table_df["FEES & COSTS($)"].notna().all()
        table_df[["FEES & COSTS($)", "PRIMARY CAUSE"]] = (
            table_df["FEES & COSTS($)"]
            .astype(str)
            .str.cat(table_df["PRIMARY CAUSE"])
            .str.extract(FEE_AND_PRIM_CASE_PAT)
        )

        # do special replacements and convert the numerical columns
        table_df["FEES & COSTS($)"] = (
            table_df["FEES & COSTS($)"].str.replace(",", "").astype(int)
        )
        table_df["PAYMENT AMOUNT($)"].replace(
            payment_amount_replacements,
            inplace=True,
        )
        table_df["PAYMENT AMOUNT($)"] = (
            table_df["PAYMENT AMOUNT($)"].str.replace(",", "").astype(float)
        )

        # now append
        raw_2009_df = raw_2009_df.append(table_df, ignore_index=True)

    # convert to datetime
    raw_2009_df["DATE TO COMPTROLLER"] = pd.to_datetime(
        raw_2009_df["DATE TO COMPTROLLER"]
    )
    # fix dtypes
    raw_2009_df = raw_2009_df.astype(raw_2009_df_col_types)
    # do whitespace fixing
    raw_2009_df = util.strip_and_trim_whitespace(raw_2009_df)

    util.save_df(
        df=raw_2009_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2009_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2009_df


def process_2010_law_website_data() -> pd.DataFrame:
    """Loads the raw 2010 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 3.
    # also make the first unskipped row the headers
    raw_2010_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2010_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2010_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=3,
    )
    # verify there are 957 rows in total
    assert raw_2010_df.shape == (957, 8)

    # fix any whitespace issues
    raw_2010_df = util.strip_and_trim_whitespace(raw_2010_df)

    util.save_df(
        df=raw_2010_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2010_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2010_df


def process_2011_law_website_data() -> pd.DataFrame:
    """Loads the raw 2011 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 4.
    # also make the first unskipped row the headers
    raw_2011_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2011_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2011_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=4,
    )
    # verify there are 935 rows in total
    assert raw_2011_df.shape == (935, 8)

    # fix any whitespace issues
    raw_2011_df = util.strip_and_trim_whitespace(raw_2011_df)

    util.save_df(
        df=raw_2011_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2011_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2011_df


def process_2012_law_website_data() -> pd.DataFrame:
    """Loads the raw 2012 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 6.
    # also make the first unskipped row the headers
    raw_2012_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2012_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2012_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=6,
    )
    # verify there are 919 rows in total
    assert raw_2012_df.shape == (919, 8)

    # split into tort and non tort
    assert raw_2012_df.loc[0, "CASE #"] == "TORT"
    assert raw_2012_df.loc[909, "CASE #"] == "NON-TORT"

    raw_2012_df.loc[0:909, "Tort Status"] = "TORT"
    raw_2012_df.loc[909:, "Tort Status"] = "NON-TORT"

    raw_2012_df.drop(index=[0, 909], inplace=True)

    # fix any whitespace issues
    raw_2012_df = util.strip_and_trim_whitespace(raw_2012_df)

    util.save_df(
        df=raw_2012_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2012_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2012_df


def process_2013_law_website_data() -> pd.DataFrame:
    """Loads the raw 2013 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 4.
    # also make the first unskipped row the headers
    raw_2013_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2013_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2013_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=4,
    )
    # verify there are 1068 rows in total
    assert raw_2013_df.shape == (1068, 9)

    # rename the last column to no name
    raw_2013_df.rename(columns={"Unnamed: 8": "Hidden Column"}, inplace=True)

    # fix any whitespace issues
    raw_2013_df = util.strip_and_trim_whitespace(raw_2013_df)

    util.save_df(
        df=raw_2013_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2013_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2013_df


def process_2014_law_website_data() -> pd.DataFrame:
    """Loads the raw 2014 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 3 rows and the last 654.
    # also make the first unskipped row the headers
    raw_2014_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2014_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2014_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=3,
        skipfooter=654,
    )
    # verify there are 1172 rows in total
    assert raw_2014_df.shape == (1172, 13)

    # drop the hidden comptroller column
    assert raw_2014_df["COMPTROLLER"].isna().all()
    raw_2014_df.drop(columns=["COMPTROLLER"], inplace=True)

    for col in ["EFFECTIVE DATE\n", "DATE TO\nCOMPTROLLER", "DUE DATE"]:
        raw_2014_df[col] = pd.to_datetime(raw_2014_df[col])

    # fix any whitespace issues
    raw_2014_df = util.strip_and_trim_whitespace(raw_2014_df)

    util.save_df(
        df=raw_2014_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2014_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2014_df


def process_2015_law_website_data() -> pd.DataFrame:
    """Loads the raw 2015 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 6.
    # also make the first unskipped row the headers
    raw_2015_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2015_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2015_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=6,
    )
    # verify there are 1172 rows in total
    assert raw_2015_df.shape == (1150, 8)

    for col in ["DATE TO\nCOMPTROLLER"]:
        raw_2015_df[col] = pd.to_datetime(raw_2015_df[col])

    # fix any whitespace issues
    raw_2015_df = util.strip_and_trim_whitespace(raw_2015_df)

    util.save_df(
        df=raw_2015_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2015_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2015_df


def process_2016_law_website_data() -> pd.DataFrame:
    """Loads the raw 2016 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 6.
    # also make the first unskipped row the headers
    raw_2016_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2016_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2016_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=6,
    )
    # verify there are 946 rows in total
    assert raw_2016_df.shape == (946, 8)

    for col in ["DATE TO\nCOMPTROLLER"]:
        raw_2016_df[col] = pd.to_datetime(raw_2016_df[col])

    # fix any whitespace issues
    raw_2016_df = util.strip_and_trim_whitespace(raw_2016_df)

    util.save_df(
        df=raw_2016_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2016_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2016_df


def process_2017_law_website_data() -> pd.DataFrame:
    """Loads the raw 2017 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 6.
    # also make the first unskipped row the headers
    raw_2017_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2017_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2017_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=6,
    )
    # verify there are 941 rows in total
    assert raw_2017_df.shape == (941, 8)

    for col in ["DATE TO\nCOMPTROLLER"]:
        raw_2017_df[col] = pd.to_datetime(raw_2017_df[col])

    # fix any whitespace issues
    raw_2017_df = util.strip_and_trim_whitespace(raw_2017_df)

    util.save_df(
        df=raw_2017_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2017_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2017_df


def process_2018_law_website_data() -> pd.DataFrame:
    """Loads the raw 2018 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 6.
    # also make the first unskipped row the headers
    raw_2018_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2018_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2018_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=6,
    )
    # verify there are 913 rows in total
    assert raw_2018_df.shape == (913, 8)

    for col in ["DATE TO\nCOMPTROLLER"]:
        raw_2018_df[col] = pd.to_datetime(raw_2018_df[col])

    # fix any whitespace issues
    raw_2018_df = util.strip_and_trim_whitespace(raw_2018_df)

    util.save_df(
        df=raw_2018_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2018_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2018_df


def process_2019_law_website_data() -> pd.DataFrame:
    """Loads the raw 2019 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 7.
    # also make the first unskipped row the headers
    raw_2019_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2019_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2019_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=7,
    )
    # verify there are 586 rows in total
    assert raw_2019_df.shape == (586, 8)

    for col in ["DATE TO\nCOMPTROLLER"]:
        raw_2019_df[col] = pd.to_datetime(raw_2019_df[col])

    # fix any whitespace issues
    raw_2019_df = util.strip_and_trim_whitespace(raw_2019_df)

    util.save_df(
        df=raw_2019_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2019_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2019_df


def process_2020_law_website_data() -> pd.DataFrame:
    """Loads the raw 2020 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 6.
    # also make the first unskipped row the headers
    raw_2020_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2020_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2020_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=6,
    )
    # verify there are 533 rows in total
    assert raw_2020_df.shape == (533, 8)

    for col in ["DATE TO\nCOMPTROLLER"]:
        raw_2020_df[col] = pd.to_datetime(raw_2020_df[col])

    # fix any whitespace issues
    raw_2020_df = util.strip_and_trim_whitespace(raw_2020_df)

    util.save_df(
        df=raw_2020_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2020_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2020_df


def process_2021_law_website_data() -> pd.DataFrame:
    """Loads the raw 2021 settlement data from the law department csv,
    converts it to a properly formatted dataframe, saves to csv and returns it
    """
    # load the excel file and skip the first 4 rows and the last 7.
    # also make the first unskipped row the headers
    raw_2021_df = pd.read_excel(
        io=DIR_C.RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR.joinpath(
            RAW_C.RAW_2021_LAW_WEBSITE_DATA_EXCEL_FILE
        ),
        sheet_name=RAW_C.RAW_2021_LAW_WEBSITE_DATA_EXCEL_SHEET,
        header=1,
        skiprows=4,
        skipfooter=7,
    )
    # drop empty columns read in for some reason
    raw_2021_df.dropna(axis=1, inplace=True, how="all")
    # verify there are 473 rows in total
    assert raw_2021_df.shape == (473, 8)

    for col in ["DATE TO COMPTROLLER"]:
        raw_2021_df[col] = pd.to_datetime(raw_2021_df[col])

    # fix any whitespace issues
    raw_2021_df = util.strip_and_trim_whitespace(raw_2021_df)

    util.save_df(
        df=raw_2021_df,
        file_name=RAW_C.RAW_CSV_FORMATTED_2021_LAW_WEBSITE_DATA_CSV,
        save_dir=DIR_C.RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR,
    )

    return raw_2021_df


def raw_law_website_processing_main() -> None:
    """Main function for the raw_law_website_data_processing module
    which creates cleaned csv versions of the data from 2008 to 2021
    """
    process_2008_law_website_data()
    process_2009_law_website_data()
    process_2010_law_website_data()
    process_2011_law_website_data()
    process_2012_law_website_data()
    process_2013_law_website_data()
    process_2014_law_website_data()
    process_2015_law_website_data()
    process_2016_law_website_data()
    process_2017_law_website_data()
    process_2018_law_website_data()
    process_2019_law_website_data()
    process_2020_law_website_data()
    process_2021_law_website_data()


if __name__ == "__main__":
    raw_law_website_processing_main()
