import csv
import requests
import json
import pandas as pd
from utils import get_api_key, get_zipcodes, get_lat_lon_from_address, write_csv_data, get_cord_distance, get_requset_data, column_as_list
from utils import get_float

CA_NPS_INFO_CSV = "nps_ca.csv"
NPS_DISTANCE_CSV = "la_nps_distance_data1.csv"

api_key = get_api_key("nps")
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
    

def get_park_distance():
    nps_names = column_as_list(CA_NPS_INFO_CSV, 'Name')
    nps_distance_header = ['zip_code', 'city(s)', 'latitue', 'longditude']
    nps_distance_header.extend(nps_names)
    # print(nps_distance_header)

    with open('../bak/la-zip.csv', 'r') as f1, open(NPS_DISTANCE_CSV, 'w') as fw:
        reader1 = csv.reader(f1)
        writer = csv.writer(fw)
        writer.writerow(nps_distance_header)        

        next(reader1)
        
        for row in reader1:
            zip_distance_data = row
            ct = len(row)
            z_lat = get_float(row[2])
            z_lon = get_float(row[3])
            z_cord = (z_lat, z_lon)

            with open(CA_NPS_INFO_CSV, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2) 
                for row2 in reader2:
                    p_name = row2[1]
                    if p_name.strip() != nps_distance_header[ct]:
                        raise Exception ("{} does not match with {}".format(p_name, nps_distance_header[ct]))
                    p_lat = row2[5]
                    p_lon = row2[6]
                    distance = None
                    if p_lat and p_lon:
                        p_cord = (get_float(p_lat), get_float(p_lon))
                        distance = get_cord_distance(z_cord, p_cord)
                    zip_distance_data.append(distance)
                    ct = ct+1
                writer.writerow(zip_distance_data)

    
def main():
    
    # create_nps_parks_data()
    get_park_distance()

if __name__ == "__main__":
    main()
