import csv
import requests
# from ../utils import get_zipcodes, get_lat_lon_from_address, write_csv_data, get_cord_distance, get_requset_data, column_as_list
# from ../utils import get_float

import pandas as pd

def get_full_address(address, city, state, zip):
    full_address = "{},{},{} {}".format(address, city, state, zip)
    print(full_address)
    return full_address

def main():
    '''
    df1 =  pd.read_csv ('NH_ProviderInfo_Jun2022.csv', sep=",", encoding='cp1252')
    df1 =  pd.read_csv ('~/Downloads/hospitals_current_data2/Timely_and_Effective_Care-Hospital.csv', sep=",", encoding='cp1252')
    df1 =  pd.read_csv ('~/Downloads/hospitals_current_data2/Complications_and_Deaths-Hospital.csv', sep=",", encoding='cp1252')
    df1 =  pd.read_csv ('~/Downloads/hospitals_current_data/Hospital_General_Information.csv', sep=",", encoding='cp1252')
    df1 =  pd.read_csv ('~/Downloads/dialysis_facilities_current_data/pdc_s3_dfc_data_bmqj_88i5.csv', sep=",", encoding='cp1252')
    df1 =  pd.read_csv ('~/David/downloaded_data/dialysis_facilities_current_data/qip1-ichc.csv', sep=",", encoding='cp1252')
    df1 =  pd.read_csv ('~/David/downloaded_data/long-term_care_hospitals_current_data/Long-Term_Care_Hospital-Provider_Data_Jun2022.csv', sep=",", encoding='cp1252')

    '''
    df1 =  pd.read_csv ('~/David/downloaded_data/inpatient_rehabilitation_facilities_current_data/Inpatient_Rehabilitation_Facility-Provider_Data_Jun2022.csv', sep=",", encoding='cp1252')
    df2 = pd.read_csv ('../zip_code_zcta.csv')
    df2.set_index('ZIP_CODE')

    df = pd.merge(left=df2, right=df1, how='left', left_on='ZIP_CODE', right_on='Zip Code')
    df.set_index('ZIP_CODE')
    print(df.head())
    df = df.iloc[: , 1:]
    df = df.sort_values(by=['ZIP_CODE'])
    #df['full_address'] = df.apply (lambda row: get_full_address(df['Address'], df['City'], df['State'], df['ZIP Code']), axis=1)
    df.to_csv("Inpatient_Rehabilitation_Facility-Provider_Data_Jun2022.csv")

main()
    
