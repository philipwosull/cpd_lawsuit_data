# Philip O'Sullivan
""" This module contains constants for processing the raw data from various
sources into csv formatted versions which can be easily worked with by
standard data processing libraries
"""

##############################################################
# ------------------------------------------------------------
# Filename Related Constants
# - Constant values for loading and saving files
# ------------------------------------------------------------
##############################################################

# ------------------------------------------------------------
# FOIA Data Filename Constants
# ------------------------------------------------------------
# unmodified raw file names
RAW_TORT_PAYMENTS_2001_TO_2007_FOIA_DATA_EXCEL_FILE = (
    "tort payments 2001 to 12312007.xlsx"
)
RAW_TORT_PAYMENTS_2001_TO_2007_FOIA_DATA_EXCEL_SHEET = "A"
RAW_CPD_PAYMENTS_2004_TO_2018_FOIA_DATA_EXCEL_FILE = "cpd_2004to2018.xlsx"
RAW_CPD_PAYMENTS_2004_TO_2018_FOIA_DATA_EXCEL_SHEET = "A"
RAW_PENDING_POLICE_SUITS_FOIA_DATA_EXCEL_FILE = "4.F_Pending_Police_Cases_Report.xlsx"
RAW_PENDING_POLICE_SUITS_FOIA_DATA_EXCEL_SHEET = "Attorney Caseload"
RAW_QUARTERLY_POLICE_SUIT_DISP_FOIA_DATA_EXCEL_FILE = (
    "5-D_Quarterly_Police_Case_Dispositions.xlsx"
)
RAW_QUARTERLY_POLICE_SUIT_DISP_FOIA_DATA_EXCEL_SHEET = "Quarterly Police Case Dispositi"

# csv formatted raw file names
RAW_CSV_FORMATTED_TORT_PAYMENTS_2001_TO_2007_FOIA_DATA_CSV = (
    "raw_csv_formatted_tort_payments_2001_to_2007_foia_data.csv"
)
RAW_CSV_FORMATTED_CPD_PAYMENTS_2004_TO_2018_FOIA_DATA_CSV = (
    "raw_csv_formatted_cpd_payments_2004_to_2018_foia_data.csv"
)
RAW_CSV_FORMATTED_PENDING_POLICE_SUITS_FOTA_DATA_CSV = (
    "raw_csv_formatted_pending_police_lawsuits_foia_data.csv"
)

# ------------------------------------------------------------
# Law Website Data Filename Constants
# ------------------------------------------------------------

# Raw data file and sheet names
RAW_2008_LAW_WEBSITE_DATA_PDF = "2008expendituresthrough12312008.pdf"
RAW_2009_LAW_WEBSITE_DATA_PDF = "2009expendituresthrough12312009.pdf"
RAW_2010_LAW_WEBSITE_DATA_EXCEL_FILE = (
    "2010_expenditures_through_12312010_accessible.xls"
)
RAW_2010_LAW_WEBSITE_DATA_EXCEL_SHEET = "A"
RAW_2011_LAW_WEBSITE_DATA_EXCEL_FILE = "2011expendituresthrough12312011.xls"
RAW_2011_LAW_WEBSITE_DATA_EXCEL_SHEET = "A"
RAW_2012_LAW_WEBSITE_DATA_EXCEL_FILE = "2012expendituresthroughdec312012.xlsx"
RAW_2012_LAW_WEBSITE_DATA_EXCEL_SHEET = "A"
RAW_2013_LAW_WEBSITE_DATA_EXCEL_FILE = "2013expendituresthrough12312013.xlsx"
RAW_2013_LAW_WEBSITE_DATA_EXCEL_SHEET = "A"
RAW_2014_LAW_WEBSITE_DATA_EXCEL_FILE = "2014ExpendituresThrough12.31.2014.xlsx"
RAW_2014_LAW_WEBSITE_DATA_EXCEL_SHEET = "A"
RAW_2015_LAW_WEBSITE_DATA_EXCEL_FILE = "2015expendituresthrough12312015.xlsx"
RAW_2015_LAW_WEBSITE_DATA_EXCEL_SHEET = "A"
RAW_2016_LAW_WEBSITE_DATA_EXCEL_FILE = "2016expendituresthrough12312016.xlsx"
RAW_2016_LAW_WEBSITE_DATA_EXCEL_SHEET = "A"
RAW_2017_LAW_WEBSITE_DATA_EXCEL_FILE = "2017expendituresthrough12312017.xlsx"
RAW_2017_LAW_WEBSITE_DATA_EXCEL_SHEET = "A"
RAW_2018_LAW_WEBSITE_DATA_EXCEL_FILE = "2018expendituresthrough12312018.xlsx"
RAW_2018_LAW_WEBSITE_DATA_EXCEL_SHEET = "2018 full report"
RAW_2019_LAW_WEBSITE_DATA_EXCEL_FILE = "Finance Cmte 2019 JS through 12.31.19.xlsx"
RAW_2019_LAW_WEBSITE_DATA_EXCEL_SHEET = "prior month ytd"
RAW_2020_LAW_WEBSITE_DATA_EXCEL_FILE = "Finance Cmte YTD thru 12.31.20.xlsx"
RAW_2020_LAW_WEBSITE_DATA_EXCEL_SHEET = "prior month ytd"
RAW_2021_LAW_WEBSITE_DATA_EXCEL_FILE = "Finace Cmte 2021 JS through 08.30.2021.xlsx"
RAW_2021_LAW_WEBSITE_DATA_EXCEL_SHEET = "Sheet1"


# csv formatted versions of the raw data
RAW_CSV_FORMATTED_2008_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2008_law_website_data.csv"
)
RAW_CSV_FORMATTED_2009_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2009_law_website_data.csv"
)
RAW_CSV_FORMATTED_2010_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2010_law_website_data.csv"
)
RAW_CSV_FORMATTED_2011_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2011_law_website_data.csv"
)
RAW_CSV_FORMATTED_2012_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2012_law_website_data.csv"
)
RAW_CSV_FORMATTED_2013_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2013_law_website_data.csv"
)
RAW_CSV_FORMATTED_2014_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2014_law_website_data.csv"
)
RAW_CSV_FORMATTED_2015_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2015_law_website_data.csv"
)
RAW_CSV_FORMATTED_2016_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2016_law_website_data.csv"
)
RAW_CSV_FORMATTED_2017_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2017_law_website_data.csv"
)
RAW_CSV_FORMATTED_2018_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2018_law_website_data.csv"
)
RAW_CSV_FORMATTED_2019_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2019_law_website_data.csv"
)
RAW_CSV_FORMATTED_2020_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2020_law_website_data.csv"
)
RAW_CSV_FORMATTED_2021_LAW_WEBSITE_DATA_CSV = (
    "raw_csv_formatted_2021_law_website_data.csv"
)
