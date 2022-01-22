# Philip O'Sullivan
""" This module contains all directory related constants for the repo.
It only uses paths relative to the repo so it can run anywhere as long
as the repo structure is not modified """

# stdlib imports
import pathlib


# directory of the entire repo, defined relative to this file
REPO_NAME = "cpd_lawsuit_data"
REPO_DIR = pathlib.Path(__file__).parent.parent

# directory with code
CODE_FOLDER = "code"
CODE_DIR = REPO_DIR / CODE_FOLDER

# Raw data directory
RAW_DATA_FOLDER = "raw_data"
RAW_DATA_DIR = REPO_DIR / RAW_DATA_FOLDER

# Raw law department website data directory
RAW_LAW_WEBSITE_DATA_FOLDER = "law_website_data"
RAW_LAW_WEBSITE_DATA_DIR = RAW_DATA_DIR / RAW_LAW_WEBSITE_DATA_FOLDER

# unmodified raw law department website data directory
RAW_UNMODIFIED_LAW_WEBSITE_DATA_FOLDER = "unmodified_raw_data"
RAW_UNMODIFIED_LAW_WEBSITE_DATA_DIR = (
    RAW_LAW_WEBSITE_DATA_DIR / RAW_UNMODIFIED_LAW_WEBSITE_DATA_FOLDER
)

# csv formatted raw law department website data directory
RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_FOLDER = "csv_formatted_raw_data"
RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_DIR = (
    RAW_LAW_WEBSITE_DATA_DIR / RAW_CSV_FORMATTED_LAW_WEBSITE_DATA_FOLDER
)

# Cleaned and standardized data directory
CLEANED_AND_STANDARDIZED_DATA_FOLDER = "cleaned_and_standardized_data"
CLEANED_AND_STANDARDIZED_DATA_DIR = REPO_DIR / CLEANED_AND_STANDARDIZED_DATA_FOLDER
