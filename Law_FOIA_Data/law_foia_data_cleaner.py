# This file cleans law department data given as response to FOIA requests

import pandas as pd
import numpy as np
from os import path

#Years to load files for - 2008 excluded
YEAR_RANGE = range(2009, 2019)
PENDING_POLICE_CASES_EXCEL = "Raw_FOIA_Data/4.F_Pending_Police_Cases_Report.xlsx"
PENDING_EXCEL_SHEET = "Attorney Caseload"
EXCEL_SHEET = "Payments"
FILE_LOCATION = "Law_Website_Raw_Data/"
FILE_BASE = "_Payments.xlsx"
ALL_SUITS_CSV_NAME = "all_lawsuits_2008_to_2018.csv"
ALL_POLICE_SUITS_CSV = "police_lawsuits_2008_to_2018.csv"
#Dictionary Reducing the Primary cause catagories for police lawsuits

def process_pending_cases():
    '''
    Processes the pending police cases excel file
    saves the claned version to a csv and returns 
    the file as a dataframe
    '''
    pending_df = pd.read_excel(PENDING_POLICE_CASES_EXCEL,"Attorney Caseload", header = 1)
    pending_df.drop(len(pending_df)-1, inplace=True)
    #Clean up allegation
    pending_df["Allegation"] = pending_df["Allegation"].str.replace('Dispute:General:Police Matters:', '')
    #Make date format better   
    pending_df["Incident Date"] = pd.to_datetime(pending_df["Incident Date"])
    pending_df["Incident Year"] = pending_df["Incident Date"].dt.year
    pending_df["Incident Month"] = pending_df["Incident Date"].dt.month
    pending_df["Incident Day"] = pending_df["Incident Date"].dt.day
    
    return pending_df



def load_annual_sheet(excel_file, sheet_name):
    '''
    Reads in the excel file and processes it

    Inputs:
        excel_file (string): path to the excel file
        sheet_name (string): the name of the sheet you want to work on

    Returns
        A pandas dataframe
    '''
    
    if not path.exists(excel_file):
        print('The file could not be found, please try again')
        return None

    dtype_dict = {'Payment Amount':float, 'Fees and Costs':float, "City Department Involved":str}
    df = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=dtype_dict)
    
    #Deals with minor formatting issues
    df["City Department Involved"] = df["City Department Involved"].str.strip()
    df["City Department Involved"] = df["City Department Involved"].str.replace(u'\xa0', u' ')
    df["City Department Involved"] = df["City Department Involved"].str.replace(' 0931', '')
    df["Primary Cause"] = df["Primary Cause"].str.replace(u'\xa0', u' ')
    df["Primary Cause"] = df["Primary Cause"].str.strip()
    df['Disposition'] = df['Disposition'].str.replace(u'\xa0', u' ')
    df['Disposition'] = df['Disposition'].str.strip()    
    
    #Seperates month and year column
    df["Date to Comptroller"] = pd.to_datetime(df["Date to Comptroller"])
    df["Year to Comptroller"] = df["Date to Comptroller"].dt.year
    df["Month to Comptroller"] = df["Date to Comptroller"].dt.month
    
    #Turns boolean values in True/False
    df.Tort.replace('YES', True, inplace=True)
    df.Tort.replace('NO', False, inplace=True)
    df.Tort.replace('NA', np.NaN, inplace=True)
    
    #Fixes mispellings in city department
    df['City Department Involved'].replace('FLEET MANAEMENT', 'FLEET MANAGEMENT', inplace=True)
    df['Disposition'].replace('OFFER OF JDGMT', 'OFFER OF JUDGMENT', inplace=True)
    df['Payment Amount(millions)'] = df['Payment Amount'] / 1000000
    df['Fees and Costs(millions)'] = df['Fees and Costs'] / 1000000
    df['Total Paid'] = df['Fees and Costs'] + df['Payment Amount']
    df['Total Paid(millions)'] = df['Total Paid'] / 1000000
    
    return df

def combine_all_dfs():
	'''
    Loads and merges dataframes for each year in year range
    plus 2008 and saves it to a CSV with all suits and just 
    police ones

    Inputs:
		Nothing

    Returns:
        Nothing
	'''
	df_total = load_annual_sheet(FILE_LOCATION+ "2008" + FILE_BASE, EXCEL_SHEET)
	#Adds the data for the years in YEAR_RANGE
	for year in YEAR_RANGE:
		full_file_name = FILE_LOCATION + str(year) + FILE_BASE
		df_total = df_total.append(load_annual_sheet(\
			full_file_name, EXCEL_SHEET), ignore_index=True, sort=False)

	#Applies the cause_map to police cases
	police_cases = df_total['City Department Involved'] == 'POLICE'
	df_total.loc[police_cases, 'Primary Cause'].map(CAUSE_MAP)
	df_total.loc[police_cases, 'Primary Cause'].fillna('Other', inplace=True)
	#Saves the cases to csvs
	df_total.to_csv(ALL_SUITS_CSV_NAME, index=False)
	df_total[police_cases].to_csv(ALL_POLICE_SUITS_CSV, index=False)
	

if __name__ == '__main__':
    combine_all_dfs()

