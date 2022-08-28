import csv
import requests
from utils import get_zipcodes, get_lat_lon_from_address, write_csv_data, get_cord_distance, get_requset_data, column_as_list
from utils import get_float, get_api_key, get_variables, get_zctas
from census import Census
from us import states
import json
import pandas as pd

def run_query():
    pass

def get_query_text(query_url):
    print(query_url)
    response = requests.get(query_url)
    return response.text

def main():

    api_key = get_api_key("census")
    # print(api_key)
    zip_codes = get_zctas()
    zips = ",".join(map(str, zip_codes))
    # print(zips)
    variables_data = get_variables("variables_2020_education.json")
    variables = list(variables_data.keys())
    header =  list(variables_data.values())
    header.append("ZCTA")
    print(variables)

    c = Census(api_key)

    df_data = []
    data = c.acs5.state_zipcode(variables, states.CA.fips, zips)
    #print(json.dumps(data[0], indent=2))
    for d in  data:
        df_data.append(list(d.values()))

    df1 = pd.DataFrame(df_data, columns=header)
    print(df1)
    df1["12th Grade or Less - No deploma"]= df1.iloc[:, 1:16].sum(axis=1)
    df1['ZCTA'] = df1.ZCTA.astype('int64')
    df1.drop(df1.columns[1:16], axis = 1, inplace=True)
    df_12 = df1["12th Grade or Less - No deploma"]
    df1.drop(labels=["12th Grade or Less - No deploma"], axis=1,inplace = True)
    df1.insert(1, "12th Grade or Less - No deploma", df_12)
    print(df1.dtypes)
   
    df2 =  pd.read_csv ('zip_code_zcta.csv')
    #print(df2.dtypes)

    df = pd.merge(left=df2, right=df1, how='left', left_on='ZCTA', right_on='ZCTA')


    #df2.merge(df1, on='ZIP_CODE', how='left')

    df.to_csv('education_data_zcta1.csv')


    

main()

