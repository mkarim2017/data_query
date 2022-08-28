import os
import pandas as pd
import requests
import urllib.parse
import csv 
from geopy.geocoders import Nominatim
from geopy import distance
import json

USER_AGENT = "DAVID"

def get_variables(var_file="variables_2020_population.json"):
    with open(var_file, "r") as f:
        data = json.load(f)
    return data

def get_api_key(account="census"):
    with open(".apikey", "r") as f:
        data = json.load(f)
    return data.get(account, None)

def get_requset_data(url, params=None):
    if params:
        response = requests.get(url, params=params)
    else:
        response = requests.get(url)
    print(response.status_code)
    return response.json()

def get_zipcodes():
    df = pd.read_csv('la-zip.csv')
    #df.set_index('ZIP_CODE', inplace=True)
    zip_codes = df['ZIP_CODE']
    #print(type(zip_codes))
    return zip_codes.tolist()

def get_zctas():
    df = pd.read_csv('zip_code_zcta.csv')
    #df.set_index('ZIP_CODE', inplace=True)
    zctas = df['ZCTA']
    #print(type(zip_codes))
    return zctas.tolist()

def column_as_list(csv_file, column_name):
    df = pd.read_csv(csv_file)
    column_val = df[column_name]
    return column_val.tolist()

def write_csv_data(file_name, data, header=None):
    with open(file_name, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        if header:
            writer.writerow(header)

        # write the data
        if data and len(data)>0:
            for d in data:
                writer.writerow(d)


def calculate_driving_distance_km(lat1, lon1, lat2, lon2):
    import osmnx as ox

    geolocator = Nominatim(user_agent=USER_AGENT)
    location = geolocator.reverse(f"{lat1}, {lon1}")
    address = location.raw['address']
    area = f"{address['city']}, {address['country']}"
    graph = ox.graph_from_place(area, network_type='drive', 
                                simplify=True)
    orig_node = ox.distance.nearest_nodes(graph, lon1, lat1)
    target_node = ox.distance.nearest_nodes(graph, lon2, lat2)
    length = nx.shortest_path_length(G=graph, source=orig_node, 
                                     target=target_node, weight='length')
    return length / 1000 # convert from m to kms


def get_float(data):
    return float("{:.4f}".format(float(data)))

def get_cord_distance(cord1, cord2, km_mi="mi"):
    if km_mi.strip().lower() == "km":
        # return float("{:.4f}".format(distance.great_circle(cord1, cord2).km))
        return round(distance.great_circle(cord1, cord2).km, 2)
    else:
         # return float("{:.4f}".format(distance.great_circle(cord1, cord2).mi))
         return round(distance.great_circle(cord1, cord2).mi, 2)

def get_lat_lon_from_address(addr):
    geolocator = Nominatim(user_agent="DAVID")
    lat = None
    lon = None

    try:
        loc = geolocator.geocode(addr)
        return loc.latitude, loc.longitude
    except Exception as err:
        print("Error processing addr : {} : {}".format(addr, str(err)))

    return lat, lon

def get_goole_api_lat_lon_from_address(addr):
    from googlemaps import GoogleMaps
    gmaps = GoogleMaps(API_KEY)
    lat, lng = gmaps.address_to_latlng(address)
    return lat, lng

if __name__ == "__main__":
    test()


    '''
    address = 'Shivaji Nagar, Bangalore, KA 560001'
    lat, lon = get_lat_lon_from_address(address)

    print("{},{}".format(lat, lon))

    '''
