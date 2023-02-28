import pandas as pd
import csv
import requests
import json
from utils import get_float, get_api_key, get_requset_data

def Average(lst):
    return sum(lst) / len(lst)

def get_data(data):
    if not data or data == "null":
        data = 0
    return data

def process_response(response):
    avg_temp = []
    min_temp = []
    max_temp = []
    humidity = []
    precip = []
    snow = []
    visibility = []
    wingust = []
    windspeed = []
    uvindex = []

    days = response["days"]
    avg_month = {}
    for d in days:
        avg_temp.append(get_data(d["temp"]))
        min_temp.append(get_data(d["tempmin"]))
        max_temp.append(get_data(d["tempmax"]))
        humidity.append(get_data(d["humidity"]))
        precip.append(get_data(d["precip"]))
        snow.append(get_data(d["snow"]))
        visibility.append(get_data(d["visibility"]))
        windspeed.append(get_data(d["windspeed"]))
        uvindex.append(get_data(d["uvindex"]))
    '''
        .append(get_data(d[""]))
        .append(get_data(d[""]))
        .append(get_data(d[""]))
        .append(get_data(d[""]))
        .append(get_data(d[""]))
        .append(get_data(d[""]))
    
    '''

    avg_month["average_temperature"] = Average(avg_temp)
    avg_month["minimum_temperature"] =  min(min_temp) 
    avg_month["maximum_temperature"] =  max(max_temp) 
    avg_month["humidity"] =  Average(humidity) 
    avg_month["precipitation"] =  Average(precip) 
    avg_month["snow"] =  Average(snow) 
    avg_month["visibility"] =  Average(visibility) 
    avg_month["windspeed"] =  Average(windspeed) 
    avg_month["uvindex"] =  Average(uvindex) 
    return avg_month


def get_weather_la(lat, lon, d1, d2, api_key):

    url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{},{}/{}/{}?key={}".format(lat, lon, d1, d2, api_key)
    print(url)
    response = get_requset_data(url)
    return process_response(response)
    
def main():

    api_key = get_api_key("timeline_weather_apikey")
    print(api_key)

    json_file = 'weather_LA_july.json'
    csv_file = 'weather_LA_july.csv'

    weathers = []
    df = pd.read_csv('zip_code_zcta2.csv')
    df = df.reset_index()

    d1 = "2024-07-01"
    d2 = "2024-07-31"
    for index, row in df.iterrows():
        try:
            zipcode = row['ZIP_CODE']
            city = row['city(s)']
            lat = row['latitue']
            lon = row['longditude']
            avg_weather = get_weather_la(lat, lon, d1, d2, api_key)
            avg_weather["City"] = city
            avg_weather["latitude"] = lat
            avg_weather["longditude"] = lon
            avg_weather["ZIP_CODE"] = zipcode
            weathers.append(avg_weather)

        except Exception as e:
            print(str(e))

    with open(json_file, 'w') as f:
        json.dump(weathers, f, indent=2, sort_keys=True)
    df = pd.read_json(json_file)
    df.to_csv(csv_file)


main()
