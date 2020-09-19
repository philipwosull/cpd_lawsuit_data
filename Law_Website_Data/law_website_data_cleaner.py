# This file cleans and combines all the yearly reports
# on costs related to settlements and judgements against the 
# City of Chicago into one csv
# https://www.chicago.gov/city/en/depts/dol.html

import pandas as pd
import numpy as np
from os import path

#Years to load files for - 2008 excluded
YEAR_RANGE = range(2009, 2019)
EXCEL_SHEET = "Payments"
FILE_LOCATION = "Law_Website_Raw_Data/"
FILE_BASE = "_Payments.xlsx"
ALL_SUITS_CSV_NAME = "all_lawsuits_2008_to_2018.csv"
ALL_POLICE_SUITS_CSV = "police_lawsuits_2008_to_2018.xlsx"
FEDERAL_SUITS_CSV = "federal_police_lawsuits_2008_to_2018.csv"
#Dictionary Reducing the Primary cause catagories for police lawsuits
CAUSES = {
    "False Arrest":['FALSE ARREST'],
    "Excessive Force": ['EXCESSIVE FORCE/MINOR', 'EXCESSIVE FORCE', \
        'EXCESSIVE FORCE/SERIOUS', 'FALSE ARREST/EXCESSIVE FORCE',\
        'EXCESSIVE FORCE/TASER'],
    "MVA/Property Damage": ['MVA/CITY VEHICLE', 'MVA - PROPERTY DAMAGE ONLY',\
            'DAMAGE TO PROPERTY DURING OPERATIONS', 'PROPERTY DAMAGE/MVA',\
            'MVA - CITY VEHICLE','STRUCK WHILE PARKED','SIDESWIPE COLLISION',\
           'MVA/ER-POLICE', 'INTER ACCIDENT-OUR UNIT STRAIGHT AHEAD',\
           'REAR-ENDED CLAIMANT', 'MVA/PEDESTRIAN','BACKING OR ROLLING BACK',\
           'MVA/PROPERTY DAMAGE','PURSUIT/OFFENDER ACCIDENT',\
            'CPD V BACKED INTO CL VEH FRONT RIGHT DAMAGE CL VEH SCHNEIDER KATHY',\
            'CPD VEH HIT CL VEH UNSPECIFIED VEH DAMAGE MENDEZ JEANNE R',\
            'CPD V HIT CL PARKED VEH LEFT SIDE DAMAGE CL VEH HIGGS MARIA',\
            'CPD HIT CL VEH IN REAR REAR END DAMAGE CL VEH TIRADO GLORIA',\
            'CPD V HIT CL VEH LEFT SIDE DAMAGE CL VEH',\
            'CPD PUSH V INTO CL VEH LEFT SIDE DAMAGE CL VEH SCHOESSLING JOHN',\
            'CPD RESCUE-CL BOAT DMGD GASH IN CL BOAT/DMG ANCHR',\
            'CL VEH HIT CPD VEH FRONT END DMG CL VEH BOKUNIEWICZ JOSEPH',\
            'CPD VEH REARENDED CL VEH UNDISCLOSED INJURIES FLAHERTY KENNETH W','HEAD ON  COLLISION',\
            'CPD PURSUIT 3 BROKEN WINDOWS', 'INTERSECTION COLLISION',\
            'CPD B/INTO CL PARKED VEH MINOR SCRATCHES FRONT END UNKN UNKN',\
            'INTER ACCIDENT-OUR UNIT TURNING LEFT','VEHICLE COLLISION - CITY VEHICLE','PROPERTY DAMAGE - OTHER',\
            'PROPERTY DAMAGED DURING OPERATIONS', 'BICYCLE ACCIDENTS','COLLIDED WITH FIXED OBJECT','MVA - PEDESTRIAN',\
            'MVA/ER - POLICE', 'PROPERTY DAMAGE - OTHER', 'PROPERTY DAMAGED DURING OPERATIONS','PROPERTY DAMAGE/OTHER',\
            'CLAIMANT HIT FOREIGN OBJECT ON ROAD', 'CLAIMANT REAR-ENDED OUR UNIT','VEHICLE DAMAGE/LOSS POUND',\
            'PURSUIT - OFFENDER ACCIDENT','MVA - PROPERTY DAMAGE BIKE','PASSING AND TURNING ACCIDENT','PURSUIT OFFENDER ACCIDENT',\
            'PURSUIT/SQUAD ACCIDENT','CPDSA'],
    "Illegal Search/Seizure": ['ILLEGAL SEARCH/SEIZURE', 'ILLEGAL SEARCH & SEIZURE'],
    "Extended Detention/Malicious Prosecution": ['EXTENDED DETENTION/MALICIOUS PROSECUTION','EXCESSIVE FORCE/MALICIOUS PROSECUTION'],
    'Burge-Related': ['EXCESSIVE FORCE/SERIOUS/BURGE REPARATIONS','BURGE REPARATIONS']
}
#Dictionary to update dataframes
CAUSE_MAP = {m:k for k, v in CAUSES.items() for m in v}

def load_annual_sheet(excel_file, sheet_name):
    '''
    Reads in the excel file and processes it

    Inputs:
        excel_file (string): path to the excel file
        sheet_name (string): the name of the sheet you want to work on

    Returns
        A pandas dataframe
    '''
    print(excel_file)
    if not path.exists(excel_file):
        print('The file could not be found, please try again')
        return None

    dtype_dict = {'Payment Amount':float, 'Fees and Costs':float, "City Department Involved":str,
    "Case Number": str}
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
    '''
    #Adds the court/division the action took place in
    df['Case Number'].fillna('missing', inplace=True)
    df['Court'] = 'other'
    df['Division'] = 'other'
    df['Year Filed'] = 0
    df = df.apply(venue_finder, axis=1, result_type='expand')
    '''
    return df

def venue_finder(row):
    '''
    Takes a row of a payments dataframe and puts the appropriate 
    court and division for the instance
    '''
    if 'L' in row['Case Number']:
        row['Court'] = 'Circuit Court of Cook County'
        row['Division'] = 'Law Division'
    elif 'M' in row['Case Number']:
        row['Court'] = 'Circuit Court of Cook County'
        row['Division'] = 'Civil Division'
    elif 'CI' in row['Case Number']:
        row['Court'] = 'Unkown'
        row['Division'] = 'Unkown'
    elif 'C' in row['Case Number']:
        row['Court'] = 'US District Court for the Northern District of Illinois'
        row['Division'] = 'Civil Case'
        case_num = row['Case Number'].split('C')[0]
        case_num = case_num.strip()
        case_num = case_num.strip('-')
        case_num = int(case_num)
        if case_num < 50:
            case_num += 2000
            row['Year Filed'] = case_num
        else:
            case_num += 1900
            row['Year Filed'] = case_num
    return row    




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
    df_total = df_total[police_cases]
    df_total['Case Number'].fillna('missing', inplace=True)
    df_total['Court'] = 'other'
    df_total['Division'] = 'other'
    df_total['Year Filed'] = 0
    df_total = df_total.apply(venue_finder, axis=1, result_type='expand')
    df_total.to_csv(ALL_POLICE_SUITS_CSV, index=False)

    federal_df = df_total[df_total['Year Filed'] > 0]
    federal_df.to_csv(FEDERAL_SUITS_CSV, index=False)
    #federal_df.groupby('Year Filed').agg({})
    #grouped = federal_df.groupby(['Year Filed']).agg(['count','nunique', 'mean']).reset_index()
    grouped = federal_df.groupby(['Year Filed']).agg({'Case Number':'nunique', 'Total Paid':'mean','Total Paid':'median'}).reset_index()

    grouped.to_csv('agged'+FEDERAL_SUITS_CSV, index=False)
    #df_total.groupby()
    
    

if __name__ == '__main__':
    combine_all_dfs()

