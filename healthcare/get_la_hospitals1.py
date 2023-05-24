import csv
import requests
from utils import get_zipcodes, get_lat_lon_from_address, write_csv_data, get_cord_distance, get_requset_data, column_as_list
from utils import get_float

h_info_header = ['name', 'address', 'latitude', 'longitude', 'medicare_provider_number', 'hospital_bed_count', 'chrch_affl_f', 'urban_location_f', 'children_hospital_f', 'updated_dt']

HOSPITAL_INFO_CSV = "la_hospitals_data1.csv"
HOSPITAL_DISTANCE_CSV = "la_hospitals_distance_data1.csv"

hospital_api = "http://www.communitybenefitinsight.org/api/get_hospitals.php?state={}"
hospital_detail_api = "http://www.communitybenefitinsight.org/api/get_hospital_data.php?hospital_id={}"

def get_hospital_info():
    zip_codes = get_zipcodes()
    print(zip_codes)
    hospital_list_data = get_requset_data(hospital_api.format("CA"))

    hospital_info = []
    for h in hospital_list_data:
        h_zip = h['zip_code'].strip()
        # print("processing {}".format(h_zip))
        if int(h_zip) in zip_codes:
            h_info = []
            h_info.append(h['name'])
            address = "{}, {}, {}, {}".format(h['street_address'], h['city'], h['state'], h_zip)
            h_info.append(address)
            lat, lon = get_lat_lon_from_address(address)
            h_info.append(lat)
            h_info.append(lon)
            
            h_info.append(h['medicare_provider_number'])
            h_info.append(h['hospital_bed_count'])
            h_info.append(h['chrch_affl_f'])
            h_info.append(h['children_hospital_f'])
            h_info.append(h['updated_dt'])
            hospital_info.append(h_info)

    write_csv_data(HOSPITAL_INFO_CSV, hospital_info, h_info_header)


def get_hospital_distance():
    hospital_names = column_as_list(HOSPITAL_INFO_CSV, 'name')
    hospital_distance_header = ['zip_code', 'city(s)', 'latitue', 'longditude']
    hospital_distance_header.extend(hospital_names)
    # print(hospital_distance_header)

    with open('la-zip.csv', 'r') as f1, open(HOSPITAL_DISTANCE_CSV, 'w') as fw:
        reader1 = csv.reader(f1)
        writer = csv.writer(fw)
        writer.writerow(hospital_distance_header)        

        next(reader1)
        
        for row in reader1:
            zip_distance_data = row
            ct = len(row)
            z_lat = get_float(row[2])
            z_lon = get_float(row[3])
            z_cord = (z_lat, z_lon)

            with open(HOSPITAL_INFO_CSV, 'r') as f2:
                reader2 = csv.reader(f2)
                next(reader2) 
                for row2 in reader2:
                    h_name = row2[0]
                    if h_name.strip() != hospital_distance_header[ct]:
                        raise Exception ("{} does not match with {}".foramt(h_name, hospital_distance_header[ct]))
                    h_lat = row2[2]
                    h_lon = row2[3]
                    distance = None
                    if h_lat and h_lon:
                        h_cord = (get_float(h_lat), get_float(h_lon))
                        distance = get_cord_distance(z_cord, h_cord)
                    zip_distance_data.append(distance)
                    ct = ct+1
                writer.writerow(zip_distance_data)

    
def main():
    #get_hospital_info()
    
    get_hospital_distance()

if __name__ == "__main__":
    main()

