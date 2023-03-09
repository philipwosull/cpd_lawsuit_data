# Philip O'Sullivan
""" This module contains important constant values for the code to standardize
and clean the various csv formatted raw data files.
"""

# ------------------------------------------------------------
# Standardized column names
# ------------------------------------------------------------

RAW_CASE_NUM_COL = "raw_case_num"
CANONICAL_CASE_NUM_COL = "canonical_case_num"
YEAR_FILED_COL = "year_filed"
YEAR_CASE_NUMBER_COL = "year_specific_case_num"
CASE_TYPE_COL = "case_type"
CASE_GOV_LEVEL_COL = "gov_level"
PAYMENT_RECIPIENT_COL = "payment_recipient"
PAYMENT_AMOUNT_COL = "payment_amount"
PAYMENT_FUND_COL = "payment_fund"
FEES_AND_COSTS_COL = "fees_and_costs"
PRIMARY_CAUSE_COL = "primary_cause"
CITY_DEPARTMENT_INVOLVED_COL = "city_department"
DISPOSITION_COL = "disposition"
DISPOSITION_DATE_COL = "disposition_date"
DATE_TO_COMPTROLLER_COL = "date_to_comptroller"
DUE_DATE_COL = "due_date"
EFFECTIVE_DATE_COL = "effective_due_date"
TORT_STATUS_COL = "tort_status"
PDF_PAGE_NUM_COL = "original_pdf_page_num"
ORIGINALLY_HIDDEN_COL = "hidden_in_raw_data"
CLIENT_DEPARTMENT_PAYMENT_COL = "client_department_payment"
DATA_SOURCE_COL = "data_source"
CASE_NAME_COL = "case_name"
INCIDENT_DATE_COL = "incident_date"
EXTENDED_DESCRIPTION_COL = "extended_description"
LAW_DEPT_MAIN_ASSIGNED_LAWYER_COL = "main_assigned_law_dept_lawyer"
LAW_DEPT_DIVISION_COL = "law_dept_division"
CITY_ROLE_IN_LAWSUIT_COL = "citys_role"
ALTERNATE_DISP_DESCRIPTION_COL = "alternate_disposition_description"


# ------------------------------------------------------------
# Law Website Data Column Rename Dict
# - Dict used to rename the columns of the raw csv formatted law
#   department data into the standardized column names
# ------------------------------------------------------------

LAW_WEBSITE_DATA_COL_STANDARDIZATION_RENAME_DICT = {
    "CASE #": RAW_CASE_NUM_COL,
    "Docket Number": RAW_CASE_NUM_COL,
    "PAYEE": PAYMENT_RECIPIENT_COL,
    "PAYMENT AMOUNT($)": PAYMENT_AMOUNT_COL,
    "PAYMENT AMOUNT ($)": PAYMENT_AMOUNT_COL,
    "Total Amount": PAYMENT_AMOUNT_COL,
    "FEES & COSTS($)": FEES_AND_COSTS_COL,
    "FEES & COSTS ($)": FEES_AND_COSTS_COL,
    "PAYMENT FUND": PAYMENT_FUND_COL,
    "PRIMARY CAUSE": PRIMARY_CAUSE_COL,
    "Allegation": PRIMARY_CAUSE_COL,
    "Category": PRIMARY_CAUSE_COL,
    "CITY DEPARTMENT INVOLVED": CITY_DEPARTMENT_INVOLVED_COL,
    "CITY DEPARTMENT": CITY_DEPARTMENT_INVOLVED_COL,
    "Client Department": CITY_DEPARTMENT_INVOLVED_COL,
    "DISPOSITION": DISPOSITION_COL,
    "DISPOSTION": DISPOSITION_COL,
    "Disposition Description": DISPOSITION_COL,
    "Disposition": DISPOSITION_COL,
    "Disposition Date": DISPOSITION_DATE_COL,
    "DATE TO COMPTROLLER": DATE_TO_COMPTROLLER_COL,
    "DUE DATE": DUE_DATE_COL,
    "EFFECTIVE DATE": EFFECTIVE_DATE_COL,
    "Tort Status": TORT_STATUS_COL,
    "pdf_page_num": PDF_PAGE_NUM_COL,
    "Hidden Column": ORIGINALLY_HIDDEN_COL,
    "CLIENT DEPARTMENT PAYMENT": CLIENT_DEPARTMENT_PAYMENT_COL,
    "Caption": CASE_NAME_COL,
    "Incident Date": INCIDENT_DATE_COL,
    "Matter Description": EXTENDED_DESCRIPTION_COL,
    "Main Assignee": LAW_DEPT_MAIN_ASSIGNED_LAWYER_COL,
    "Division": LAW_DEPT_DIVISION_COL,
    "Role": CITY_ROLE_IN_LAWSUIT_COL,
    "Description": ALTERNATE_DISP_DESCRIPTION_COL,
}

# ------------------------------------------------------------
# Standardized special column values
# ------------------------------------------------------------
# Tort status related
TORT_TYPE = "TORT"
NON_TORT_TYPE = "NON-TORT"
# Specific filing venue related
FEDERAL_CIVIL_CASE_TYPE = "federal_civil_court"
LAW_DIV_CASE_TYPE = "law_division"
MUNICIPAL_DIV_CASE_TYPE = "municipal_division"
CITY_ADMIN_CLAIM_CASE_TYPE = "city_admin_claim"
SPECIAL_CASE_TYPE = "special"
OTHER_CASE_TYPE = "unknown_case_type"
# Filing level of government (federal, county, city)
FEDERAL_LEVEL_TYPE = "federal_court"
MUNICIPAL_LEVEL_TYPE = "cook_county_court"
CITY_LEVEL_TYPE = "city_of_chicago_body"
OTHER_LEVEL = "unknown_gov_level"
SPECIAL_LEVEL = "special"

# ------------------------------------------------------------
# File Names
# - Dicts used to rename the columns of the raw csv formatted law
#   department data into the standardized column names
# ------------------------------------------------------------

# Law website related
STANDARDIZED_2008_LAW_WEBSITE_DATA_CSV = "standardized_2008_law_website_data.csv"
STANDARDIZED_2009_LAW_WEBSITE_DATA_CSV = "standardized_2009_law_website_data.csv"
STANDARDIZED_2010_LAW_WEBSITE_DATA_CSV = "standardized_2010_law_website_data.csv"
STANDARDIZED_2011_LAW_WEBSITE_DATA_CSV = "standardized_2011_law_website_data.csv"
STANDARDIZED_2012_LAW_WEBSITE_DATA_CSV = "standardized_2012_law_website_data.csv"
STANDARDIZED_2013_LAW_WEBSITE_DATA_CSV = "standardized_2013_law_website_data.csv"
STANDARDIZED_2014_LAW_WEBSITE_DATA_CSV = "standardized_2014_law_website_data.csv"
STANDARDIZED_2015_LAW_WEBSITE_DATA_CSV = "standardized_2015_law_website_data.csv"
STANDARDIZED_2016_LAW_WEBSITE_DATA_CSV = "standardized_2016_law_website_data.csv"
STANDARDIZED_2017_LAW_WEBSITE_DATA_CSV = "standardized_2017_law_website_data.csv"
STANDARDIZED_2018_LAW_WEBSITE_DATA_CSV = "standardized_2018_law_website_data.csv"
STANDARDIZED_2019_LAW_WEBSITE_DATA_CSV = "standardized_2019_law_website_data.csv"
STANDARDIZED_2020_LAW_WEBSITE_DATA_CSV = "standardized_2020_law_website_data.csv"
STANDARDIZED_2021_LAW_WEBSITE_DATA_CSV = "standardized_2021_law_website_data.csv"

STANDARDIZED_ALL_YEARS_LAW_WEBSITE_DATA_CSV = (
    "standardized_2008_to_2021_law_website_data.csv"
)

# FOIA related
STANDARDIZED_CPD_PAYMENTS_2004_TO_2018_FOIA_DATA_CSV = (
    "standardized_cpd_payments_2004_to_2018_foia_data.csv"
)
STANDARDIZED_TORT_PAYMENTS_2001_TO_2007_FOIA_DATA_CSV = (
    "standardized_tort_payments_2001_to_2007_foia_data.csv"
)
STANDARDIZED_PENDING_POLICE_SUITS_FOTA_DATA_CSV = (
    "standardized_pending_police_lawsuits_foia_data.csv"
)
STANDARDIZED_QUARTERLY_POLICE_SUIT_DISP_FOIA_DATA_CSV = (
    "standardized_quarterly_police_suit_dispositions_foia_data.csv"
)
STANDARDIZED_MATTER_DISP_REPORT_BY_DIVISION_FOIA_DATA_CSV = (
    "standardized_matter_disposition_reports_by_division_foia_data.csv"
)
STANDARDIZED_MATTER_DISP_REPORT_BY_DEPARTMENT_FOIA_DATA_CSV = (
    "standardized_matter_disposition_reports_by_department_foia_data.csv"
)
STANDARDIZED_MATTER_DISP_REPORT_BY_ASSIGNEE_FOIA_DATA_CSV = (
    "standardized_matter_disposition_reports_by_assignee_foia_data.csv"
)
