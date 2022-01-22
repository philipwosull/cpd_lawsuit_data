# CPD_Lawsuits
## What is this?
This repository contains data on lawsuits filed against the Chicago Police Department (CPD) and its officers and payments stemming from those lawsuits. It also contains code which transforms and processes the raw data into an easy to work with analysis dataset.

In the future a basic exploration of the data will be included as well.

## What Data is in here?
### Judgement and Settlement Payment Requests (2008-2021)
For each year since 2008 the City of Chicago Law Department has maintained a table of all Judgement and Settlement Payment Requests on the following website: https://www.chicago.gov/city/en/depts/dol.html. These tables contains information on legal cases and administrative claims filed involving the City of Chicago where the City was required to make a payment (or in a small minority of cases received a payment) in that year. Although the tables's columns vary somewhat from year to year typically each row in a table corresponds to a payment made to a specific person or entity stemming from a specific case/claim. This usually entails a case number, payee, the amount the city paid, the city department involved, a brief description of the reason for payment, and either the date of the payment or the date the payment was reported.
The following files stored in /raw_data/law_website_data/unmodified_raw_data were most recently downloaded from https://www.chicago.gov/city/en/depts/dol.html on the following dates:
- 2008expendituresthrough12312008.pdf 
	Most recently downloaded on 12/21/2021
- 2009expendituresthrough12312009.pdf
	Most recently downloaded on 12/21/2021
- 2010_expenditures_through_12312010_accessible.xls
	Most recently downloaded on 12/21/2021
- 2011expendituresthrough12312011.xls
	Most recently downloaded on 12/21/2021
- 2012expendituresthroughdec312012.xlsx
	Most recently downloaded on 12/21/2021
- 2013expendituresthrough12312013.xlsx
	Most recently downloaded on 12/21/2021
- 2014ExpendituresThrough12.31.2014.xlsx
	Most recently downloaded on 12/21/2021
- 2015expendituresthrough12312015.xlsx
	Most recently downloaded on 12/21/2021
- 2016expendituresthrough12312016.xlsx
	Most recently downloaded on 12/21/2021
- 2017expendituresthrough12312017.xlsx
	Most recently downloaded on 12/21/2021
- 2018expendituresthrough12312018.xlsx
	Most recently downloaded on 12/21/2021
- Finance Cmte 2019 JS through 12.31.19.xlsx
	Most recently downloaded on 12/21/2021
- Finance Cmte YTD thru 12.31.20
	Most recently downloaded on 12/21/2021
- Finace Cmte 2021 JS through 08.30.2021.xlsx
	Most recently downloaded on 12/23/2021

### Law Department FOIA Response Data
In 2019 the creator of this repository submitted various FOIA requests to the City of Chicago Law Department to attempt to obtain settlement and judgement data similiar to the ones available on the Law Department's website but for years before 2008. The Law Department responded with various excel files with records as far back at 2001. 
The raw unmodified files received in response to the FOIA requests are stored in /raw_data/foia_data/unmodified_raw_foia_data. The FOIA requests submitted are stored in /raw_data/foia_data/foia_requests (personal information has been redacted.)

### Historical 42 US Code § 1983 Lawsuit Data (1957 to 1967)
This portion contains data on civil suits filed under 42 US Code § 1983 (commonly referred to as Section 1983 suits) in the United States District Court for the Northern District of Illinois from 1957 to 1967 against the CPD or its officers. This data was gathered as part of archival research for a paper on the CPD, police torture and abusive detention practices, and Section 1983 in late 50s/60s era Chicago. More information on how this data was collected can be found [in footnote 33 of this paper.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3924502)

The creator of this repository would like to thank AK Alilonu and Valerie Han for their assistance in the archival research and Micah Clark Moody, Zachary Garai, Richard Lin, Bernadette Looney, and Wesley Chen for their assistance in coding this dataset. 

## Repository Structure
The repository has the following important folders:
- code - This folder contains all the code used to clean and transform the raw data into the analysis dataset and all relevant intermediary forms.
- raw_data - This folder contains all the 'raw data', i.e. data in the original format received or only slightly transformed into an easier to work with csv format.
- cleaned_and_standardized_data - This folder contains data from the raw_data folder that has been cleaned and relevant values and column names have been standardized. 

In the future work will be done on creating an analysis dataset and a database combining all the three data sources.