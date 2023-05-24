import os
import csv
import requests
import json
import pandas as pd
from utils import get_api_key, get_zipcodes, get_lat_lon_from_address, write_csv_data, get_cord_distance, get_requset_data, column_as_list
from utils import get_float

CA_NPS_INFO_CSV = "LA_Parks.csv"
NPS_DISTANCE_CSV = "LA_Parks_distance_data1.csv"

#api_key = get_api_key("nps")
#params = {'apikey' : api_key}
params = None

nps_api_root = "https://developer.nps.gov/api/v1"
json_file = "nps_ca.json"
csv_file = "nps_ca.csv"

def get_address(addresses):
    adrr_json = addresses[0]
    addr = ""
    if "line1" in adrr_json and len(adrr_json["line1"]) > 0:
        addr = "{},".format(adrr_json["line1"])
        
    if "line2" in adrr_json and len(adrr_json["line2"]) > 0:
        addr = "{}{},".format(addr, adrr_json["line2"])

    if "line3" in adrr_json and len(adrr_json["line3"]) > 0:
        addr = "{}{},".format(addr, adrr_json["line3"])

    if "city" in adrr_json and len(adrr_json["city"]) > 0:
        addr = "{}{},".format(addr, adrr_json["city"])

    if "stateCode" in adrr_json and len(adrr_json["stateCode"]) > 0:
        addr = "{}{}".format(addr, adrr_json["stateCode"])

    if "postalCode" in adrr_json and len(adrr_json["postalCode"]) > 0:
        addr = "{} {},".format(addr, adrr_json["postalCode"])

    return addr


def create_nps_parks_data(state="CA"):

    ca_nps_array = []
    print("{}".format(api_key))
    api_url = "{}/parks?stateCode={}&api_key={}".format(nps_api_root, state, api_key)
    print(api_url)

    response = get_requset_data(api_url, params=params)
    data = response["data"]

    for np in data:
        nps = {}
        print(np.keys())
        nps["Name"] = np['fullName']
        nps["id"] = np["id"]
        nps["parkCode"] = np["parkCode"]
        nps["address"] = get_address(np['addresses'])
        nps['latitude'] = np['latitude']
        nps['longitude'] = np['longitude']
        nps['activities'] = ",".join([act["name"] for act in np['activities']])
        ca_nps_array.append(nps)
 
    with open(json_file, 'w') as f:
        json.dump(ca_nps_array, f, indent=2, sort_keys=True)

    df = pd.read_json(json_file)
    df.to_csv(csv_file)
    

def get_la_park_distance():
    rec_name = '../data/recreation/LA_Parks.csv'
    nps_names = column_as_list(rec_name, 'Park Name')
    rec_distance_header = ['zip_code', 'city(s)', 'latitue', 'longditude', 'zcta']
    rec_distance_header.extend(nps_names)
    print(rec_distance_header)

    with open('../zcta/zip_code_zcta_data.csv', 'r') as f1, open('LA_Parks_distance_data1.csv', 'w') as fw:
        reader1 = csv.reader(f1)
        writer = csv.writer(fw)
        writer.writerow(rec_distance_header)        

        next(reader1)
        
        for row in reader1:
            zip_distance_data = row
            ct = len(row)
            z_lat = get_float(row[2])
            z_lon = get_float(row[3])
            z_cord = (z_lat, z_lon)

            with open(rec_name, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2) 
                for row2 in reader2:
                    print(row2)
                    p_name = row2[1]
                    if p_name.strip() != rec_distance_header[ct]:
                        raise Exception ("{} does not match with {}".format(p_name, rec_distance_header[ct]))
                    p_lat = row2[3]
                    p_lon = row2[4]
                    distance = None
                    if p_lat and p_lon:
                        p_cord = (get_float(p_lat), get_float(p_lon))
                        distance = get_cord_distance(z_cord, p_cord)
                    zip_distance_data.append(distance)
                    ct = ct+1
                writer.writerow(zip_distance_data)


def get_la_golf_courses_distance():
    rec_data = 'LA_GOLF_COURSES.csv'
    rec_distance_data = "{}_distance_data.csv".format(rec_data.split( ".")[0])
    nps_names = column_as_list(rec_data, 'Name')
    rec_distance_header = ['zip_code', 'city(s)', 'latitue', 'longditude', 'zcta']
    rec_distance_header.extend(nps_names)
    print(rec_distance_header)

    with open('../zcta/zip_code_zcta_data.csv', 'r') as f1, open(rec_distance_data, 'w') as fw:
        reader1 = csv.reader(f1)
        writer = csv.writer(fw)
        writer.writerow(rec_distance_header)

        next(reader1)

        for row in reader1:
            zip_distance_data = row
            ct = len(row)
            z_lat = get_float(row[2])
            z_lon = get_float(row[3])
            z_cord = (z_lat, z_lon)

            with open(rec_data, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2)
                for row2 in reader2:
                    print(row2)
                    p_name = row2[1]
                    if p_name.strip() != rec_distance_header[ct]:
                        raise Exception ("{} does not match with {}".format(p_name, rec_distance_header[ct]))
                    p_lat = row2[3]
                    p_lon = row2[4]
                    distance = None
                    if p_lat and p_lon:
                        p_cord = (get_float(p_lat), get_float(p_lon))
                        distance = get_cord_distance(z_cord, p_cord)
                    zip_distance_data.append(distance)
                    ct = ct+1
                writer.writerow(zip_distance_data)



def get_la_water_resources_distance():
    rec_data = '../data/recreation/LA_Water_Resources.csv'
    rec_distance_data = "{}_distance_data.csv".format(os.path.basename(rec_data).split( ".")[0])
    print(rec_distance_data)
    nps_names = column_as_list(rec_data, 'Name')
    rec_distance_header = ['zip_code', 'city(s)', 'latitue', 'longditude', 'zcta']
    rec_distance_header.extend(nps_names)
    print(rec_distance_header)

    with open('../zcta/zip_code_zcta_data.csv', 'r') as f1, open(rec_distance_data, 'w') as fw:
        reader1 = csv.reader(f1)
        writer = csv.writer(fw)
        writer.writerow(rec_distance_header)

        next(reader1)

        for row in reader1:
            zip_distance_data = row
           
            ct = len(row)
           
            z_lat = get_float(row[2])
            z_lon = get_float(row[3])
            z_cord = (z_lat, z_lon)

            with open(rec_data, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2)
                for row2 in reader2:
                   
                    print(row2)
                    p_name = row2[1]
                    if p_name.strip() != rec_distance_header[ct]:
                        raise Exception ("{} does not match with {}".format(p_name, rec_distance_header[ct]))
                    p_lat = row2[3]
                    p_lon = row2[4]
                    distance = None
                    if p_lat and p_lon:
                        p_cord = (get_float(p_lat), get_float(p_lon))
                        distance = get_cord_distance(z_cord, p_cord)
                    zip_distance_data.append(distance)
                    ct = ct+1
                writer.writerow(zip_distance_data)


def get_la_water_resources_distance_la_almanac():
    rec_data = '../data/recreation/LA_County_Lakes_LAAlmanac.csv'
    rec_distance_data = "{}_distance_data.csv".format(os.path.basename(rec_data).split( ".")[0])
    print(rec_distance_data)
    nps_names = column_as_list(rec_data, 'Name')
    rec_distance_header = ['zip_code', 'city(s)', 'latitue', 'longditude', 'zcta']
    rec_distance_header.extend(nps_names)
    print(rec_distance_header)

    with open('../zcta/zip_code_zcta_data.csv', 'r') as f1, open(rec_distance_data, 'w') as fw:
        reader1 = csv.reader(f1)
        writer = csv.writer(fw)
        writer.writerow(rec_distance_header)

        next(reader1)

        for row in reader1:
            zip_distance_data = row

            ct = len(row)

            z_lat = get_float(row[2])
            z_lon = get_float(row[3])
            z_cord = (z_lat, z_lon)

            with open(rec_data, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2)
                for row2 in reader2:

                    print(row2)
                    p_name = row2[1]
                    if p_name.strip() != rec_distance_header[ct]:
                        raise Exception ("{} does not match with {}".format(p_name, rec_distance_header[ct]))
                    p_lat = row2[3]
                    p_lon = row2[4]
                    distance = None
                    if p_lat and p_lon:
                        p_cord = (get_float(p_lat), get_float(p_lon))
                        distance = get_cord_distance(z_cord, p_cord)
                    zip_distance_data.append(distance)
                    ct = ct+1
                writer.writerow(zip_distance_data)

def get_la_county_beaches_distance():
    rec_data = '../data/recreation/LA_County_Beaches.csv'
    rec_distance_data = "{}_distance_data.csv".format(os.path.basename(rec_data).split( ".")[0])
    print(rec_distance_data)
    nps_names = column_as_list(rec_data, 'Name')
    rec_distance_header = ['zip_code', 'city(s)', 'latitue', 'longditude', 'zcta']
    rec_distance_header.extend(nps_names)
    print(rec_distance_header)

    with open('../zcta/zip_code_zcta_data.csv', 'r') as f1, open(rec_distance_data, 'w') as fw:
        reader1 = csv.reader(f1)
        writer = csv.writer(fw)
        writer.writerow(rec_distance_header)

        next(reader1)

        for row in reader1:
            zip_distance_data = row

            ct = len(row)

            z_lat = get_float(row[2])
            z_lon = get_float(row[3])
            z_cord = (z_lat, z_lon)

            with open(rec_data, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2)
                for row2 in reader2:

                    # print(row2)
                    p_name = row2[1]
                    if p_name.strip() != rec_distance_header[ct]:
                        raise Exception ("{} does not match with {}".format(p_name, rec_distance_header[ct]))
                    p_lat = row2[3]
                    p_lon = row2[4]
                    distance = None
                    if p_lat and p_lon:
                        p_cord = (get_float(p_lat), get_float(p_lon))
                        distance = get_cord_distance(z_cord, p_cord)
                    zip_distance_data.append(distance)
                    ct = ct+1
                writer.writerow(zip_distance_data)

def remove_distant_resources(df, zcta, max_val):

    df = df[df['zcta']==zcta]
    if len(df.index) > 1:
            raise Exception("More than one row with zcta value : {}".format(zcta))
    df = df.drop(df.columns[[0, 1, 2, 3, 4]], axis=1)

    df = df.astype(float)
    print(df)

    c = []
    d = []

    resources = ""
    for col in df.columns:
        if df[col].sum() > max_val: # or df[col].isnull().values.any():
            # print("{} : {}".format(col, df[col].sum()))
            c.append(col)
        elif df[col].isnull().sum() > 0:
            print("{} is NULL : {}".format(col, df[col].isnull().sum()))
        else:
            print("{} : {}".format(col, df[col].sum()))
            if resources == "":
                resources = "{}".format(col.strip().replace(',', ':'))
            else:
                resources = resources +"; {}".format(col.strip().replace(',', ':'))
            d.append(col)
    print(resources) 
    
    return resources

def get_df(f):
    df = pd.read_csv(f)
    df_clean = df[df['zip_code'] == df['zcta']]
    return df_clean
  
def combine():
    rec_data = 'LA_COUNTY_RECREATION.csv'

    zip_data = '../zcta/zip_code_zcta2.csv'
    beach_data = '../data/recreation/LA_County_Beaches_distance_data.csv'  
    water_resources_data = '../data/recreation/LA_County_Lakes_LAAlmanac_distance_data.csv'
    park_data = '../data/recreation/LA_Parks_distance_data1.csv'
    golf_data = '../data/recreation/LA_GOLF_COURSES_distance_data.csv'

    rec_distance_header = ['city(s)', 'latitue', 'longditude', 'zcta', 'Beaches in 20 miles', 'golf courses in 10 miles' ]
    zctas = column_as_list(zip_data, 'ZCTA')
    # print(zctas)

    df = pd.read_csv(zip_data)
    df_beach = get_df(beach_data)
    df_golf = get_df(golf_data)
    df_lakes = get_df(water_resources_data)
    df_parks = get_df(park_data)
    

    data = []
    for index, row in df.iterrows():
    #for row in df.rows:
        m = {}
        m['ZCTA'] = row['ZCTA']
        m['City'] = row['city(s)']
        m['LAT'] = row['latitude']
        m['LON'] = row['longitude']
        m['Parks in 5 Miles'] = remove_distant_resources(df_parks, m['ZCTA'], 5.5)
        m['Beaches in 20 Miles'] = remove_distant_resources(df_beach, m['ZCTA'], 20.5)
        m['Golf Courses in 5 Miles'] = remove_distant_resources(df_golf, m['ZCTA'], 5.5)
        m['Lakes/Water Resources in 5 Miles'] = remove_distant_resources(df_lakes, m['ZCTA'], 5.5)


        data.append(m)

        print(json.dumps(m, indent=2))
    with open("LA_COUNTY_RECREATION.json", "w") as f:
        json.dump(data, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_COUNTY_RECREATION.json')
    df.to_csv('LA_COUNTY_RECREATION.csv') 
        
      
def main():
    
    # create_nps_parks_data()
    # get_la_park_distance()
    # get_la_golf_courses_distance()
    # get_la_water_resources_distance()
    # get_la_county_beaches_distance()
    # get_la_water_resources_distance_la_almanac()
    combine()

if __name__ == "__main__":
    main()
