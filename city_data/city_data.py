import os
import sys
import csv
from lxml import html
from bs4 import BeautifulSoup
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import requests
from utils import get_zipcodes, get_lat_lon_from_address, write_csv_data, get_cord_distance, get_requset_data, column_as_list
from utils import get_float, get_api_key, get_variables, get_zctas
import json
import re
import pandas as pd
from pprint import pprint

def get_city_data(zcode):

    url = "http://www.city-data.com/zips/{}.html".format(zcode)
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    city_data = {
      "zip_code" : zcode,
      "population" : "NA",
      "Houses_and_Condos" : "NA",
      "Renter_occupied_apartments" : "NA",
      "Cost_of_Living_Index_2019": "NA",
      "Land_Area" : "NA",
      "Water_Area": "NA",
      "Estimated_median_house_condo_value_2019" : "NA",
      "Estimated_median_Detached_House_Price_2019": "NA",
      "Estimated_median_Townhome_Condo_Price_2019": "NA",
      "Estimated_median_rent_2019": "NA",
      #"Average_Adjusted_Gross_Income_2012" : "NA",
      "Population_Density_per_Square_Mile" : "NA"
    }

    try:
        city_data["population"] = soup.body.findAll(text='Estimated zip code population in 2019:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))

    try:  
        city_data["Houses_and_Condos"] = soup.body.findAll(text='Houses and condos:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))


    try:
        city_data["Renter_occupied_apartments"] = soup.body.findAll(text='Renter-occupied apartments:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))

    

    try:
        city_data["Cost_of_Living_Index_2019"] = soup.body.findAll(text=(re.compile('March 2019 cost of living index in zip code (\d)+:')))[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))
 
    try:
        city_data["Land_Area"] = soup.body.findAll(text='Land area:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e)) 

    try:
        city_data["Water_Area"] = soup.body.findAll(text='Water area:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))
    try:
        city_data["Estimated_median_house_condo_value_2019"] = soup.body.findAll(text='Estimated median house/condo value in 2019:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))

    try:
        city_data["Estimated_median_Detached_House_Price_2019"] = soup.body.findAll(text='Detached houses:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))

    try:
        city_data["Estimated_median_Townhome_Condo_Price_2019"] = soup.body.findAll(text='Townhouses or other attached units:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))

    try:
        city_data["Estimated_median_rent_2019"] = soup.body.findAll(text='Median gross rent in 2019:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))


    '''
    try:
        city_data["Average_Adjusted_Gross_Income_2012"] = soup.body.findAll(text='Average Adjusted Gross Income (AGI) in (\d)+:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))
    '''

    try:
        city_data["Population_Density_per_Square_Mile"] = soup.body.findAll(text='Population density:')[0].find_next(text = True).replace(',', '')
    except Exception as e:
        print(str(e))

    print(json.dumps(city_data, indent=2))
    '''
    pattern = re.compile(r'<b>Estimated zip code population in 2019:<\/b> (\d+)(,)?(\d+)')
    print(pattern)
    print(soup.body.findAll(text=pattern))
    # pprint(soup.find(text=pattern).__dict__)
    for elem in soup(text='Estimated zip code population in 2019:'):
        print(elem.parent)
        print(elem.find_next(text = True))
        #nextSiblings = elem.parent.find_next_siblings("b")
        #print(nextSiblings)
    '''
    return city_data

def main():

    
    city_info = []
    zip_codes = get_zctas()
    new_zip_codes = []
    dup_zip_codes = []
    for z in zip_codes:
        if z not in new_zip_codes:
            new_zip_codes.append(z)
            try:
                city_data = get_city_data(z)
                city_info.append(city_data)
            except Exception as e:
                print(str(e))
        else:
            dup_zip_codes.append(z)

        
    print(dup_zip_codes)

    with open("LA_COUNTY_CITY_DATA.json", "w") as f:
        json.dump(city_info, f, indent=2, sort_keys=True)
   

    df1 = pd.read_json('LA_COUNTY_CITY_DATA.json')
    df2 =  pd.read_csv ('zip_code_zcta.csv')

    df = pd.merge(left=df2, right=df1, how='left', left_on='ZCTA', right_on='zip_code')

    df.to_csv('LA_COUNTY_CITY_DATA2.csv') 



main()
