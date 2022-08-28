import csv
import requests
from utils import get_zipcodes, get_lat_lon_from_address, write_csv_data, get_cord_distance, get_requset_data, column_as_list
from utils import get_float, get_api_key



def run_query():
    pass

def get_query_text(query_url):
    print(query_url)
    response = requests.get(query_url)
    return response.text

def main():

    api_key = get_api_key("census")
    print(api_key)
    zip_codes = get_zipcodes()
    zips = ",".join(map(str, zip_codes))
    print(zips)

    data = 'B01001_002E,B01001_003E,B01001_004E,B01001_005E,B01001_006E,B01001_007E,B01001_008E,B01001_009E,B01001_010E,B01001_011E,B01001_012E,B01001_013E,B01001_014E,B01001_015E,B01001_016E,B01001_017E,B01001_018E,B01001_019E,B01001_020E,B01001_021E,B01001_022E,B01001_023E'

    query_url = 'https://api.census.gov/data/2020/acs/acs5?get=B01001_002E&for=zcta:{}&in=state:06&key={}'.format(zips, api_key)
    response = get_query_text(query_url)
    print(response)
    

main()
