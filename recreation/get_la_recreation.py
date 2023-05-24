import csv
import requests
import json
import pandas as pd
from utils import get_api_key, get_zipcodes, get_lat_lon_from_address, write_csv_data, get_cord_distance, get_requset_data, column_as_list
from utils import get_float

# source = https://www.communitybenefitinsight.org/?page=info.data_api


api_key = get_api_key("recreation")
params = {'apikey' : api_key}

recreation_api_root  = "https://ridb.recreation.gov/api/v1/"

def get_facilities_by_lat_lon(lat, lon):
    api_url = "https://ridb.recreation.gov/api/v1/facilities?limit=50&offset=0&state=CA&latitude={}&longitude={}&radius=10".format(lat,lon)
    json_file = 'rec_fact.json'
    csv_file = 'rec_fact.csv'

    response = get_requset_data(api_url, params=params)
    print(json.dumps(response, indent=2))
    '''
    with open(json_file, 'w') as f:
        json.dump(response["RECDATA"], f, indent=2, sort_keys=True)
    
    df = pd.read_json(json_file)
    df.to_csv(csv_file)   
    
    #print(json.dumps(response, indent=2))
    '''

def get_recreation_data(activity_id=None, activity_name=None):
    api_url = "{}/activities".format(recreation_api_root)
    json_file = 'recreations.json'
    csv_file = 'recreation_data.csv'

    if activity_id:
        api_url = "{}/{}".format(api_url, activity_id)
        json_file = 'recreation_{}.json'.format(activity_name)
        csv_file = 'recreation_data_{}.csv'.format(activity_name)

    response = get_requset_data(api_url, params=params)
    with open(json_file, 'w') as f:
        json.dump(response["RECDATA"], f, indent=2, sort_keys=True)

    df = pd.read_json(json_file)
    df.to_csv(csv_file)



    
def main():
    #get_recreation_data(14, 'HIKING')
    get_facilities_by_lat_lon(33.76935425, -118.1845288)

if __name__ == "__main__":
    main()

