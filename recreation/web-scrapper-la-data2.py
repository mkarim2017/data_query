import requests
from lxml import html
from bs4 import BeautifulSoup
import csv
import re
import json
import pandas as pd
from time import sleep
from urllib.parse import urljoin
from utils import get_lat_lon_from_address
base_url = "https://www.laparks.org"


def get_location(URL):
    lat_lon = ";"
    page = requests.get(URL)
    # print(page.text)
    soup = BeautifulSoup(page.text, "html.parser")
    try:
        #geo = soup.find('div', class_="mw-parser-outpaut").find_all('span', class_='geo')
        geo = soup.find_all('span', class_='geo')
        lat_lon = geo[0].text.strip()
        print(lat_lon)
    except Exception as err:
        print("{} : {}".format(str(err), geo))
    return lat_lon



def get_la_county_lakes_laalmanac():
    URL = "https://www.laalmanac.com/geography/ge02.php"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    content = soup.find('div', class_="content-box")
    blist = content.find('table').find_all('tbody')
    # print(list)
    lakes = []

    for bl in blist:
        list = bl.find_all('tr')
        for l in list:
            locality = ""
            try:
                m = {}
                data = l.find_all('td')
                i=0
                m["Name"] = data[i].text.strip()
                i = i+1
                m["Address"] = ""
                m["Type"] = data[i].text.strip()
                i =i +1
                m["Surface Area"] = data[i].text.strip()
                m["Activities"] = ""
                m["Facilities"] = ""

                '''
                try:
                    href = l.find('a').get('href')
                except:
                    href = ""

                if len(href)>0:
                    get_beach_details(href)

                lat=""
                lon=""
                try:
                    lat, lon = get_lat_lon_from_address(m["Address"])
                except Exception as err:
                    print(str(err))
                m["lat"] = lat
                m["lon"] = lon
                m["href"] = href
                '''
                print(json.dumps(m, indent=2))
                lakes.append(m)
            except Exception as err:
                print(str(err))

    with open("LA_County_Lakes_LAAlmanac.json", "w") as f:
        json.dump(lakes, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_County_Lakes_LAAlmanac.json')
    df.to_csv('LA_County_Lakes_LAAlmanac.csv')


def get_water_resources():
    URL = "https://www.laparks.org/aquatic/lakes-fishing-beaches"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    tables = soup.find_all('table', class_="table-striped")

    resources = []
    for table in tables:
        thead = table.find('thead').find_all('tr')[0].text.strip()
        if 'Symbol Key' not in thead:
            rows = table.find('tbody').find_all('tr')[2:]
            for row in rows:
                try:
                    resource = {}
                    data = row.find_all('td')
                    resource["Name"] = data[0].text.strip()
                    resource["Address"] = data[1].text.strip()
                    resource['Type'] = thead
                    resource['href'] = urljoin(base_url, data[0].find('a').get('href'))
                    resources.append(resource)
                    #print(json.dumps(resource, indent=2))
                except Exception as err:
                    print(str(err))    

    print(json.dumps(resources, indent=2))
    with open("LA_Water_Resources.json", "w") as f:
        json.dump(resources, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_Water_Resources.json')
    df.to_csv('LA_Water_Resources.csv')
               
            
def get_la_cities():
    with open('../bak/la-zip.csv', 'r') as f1, open("la-cities.csv", 'w') as fw:
        reader1 = csv.reader(f1)
        writer = csv.writer(fw)
        #writer.writerow(hospital_distance_header)

        next(reader1)
        la_cities = []
        for row in reader1:
            zip_distance_data = row
            ct = len(row)
            z_cities = row[1].split('/')
            for z_c in z_cities:
                if z_c not in la_cities:
                    la_cities.append(z_c)

    return la_cities   
                 
def main():
    # get_la_county_parks_laalmanac()
    # get_la_county_beaches()
    # get_state_parks_la_county()
    # get_municipal_parks_la_city2()
    # get_state_parks_la_city2()
    # get_parks_la_county()
    # get_ca_museums()
    # get_county_museums("Orange", "https://en.wikipedia.org/wiki/List_of_museums_in_Orange_County,_California")
    #get_la_county_museums()
    #get_la_museums()

    # get_parks_la_city()
    #get_water_resources()
    #get_golf_courses()
    #get_city_data('Yorba Linda')
    get_la_county_lakes_laalmanac()

    '''
    la_park_stat = []
    la_cities = get_la_cities()
    for l_c in get_la_cities():
        la_park_stat.append(get_city_data(l_c, "California"))

    with open('la_park_stat.json', 'w') as f:
        json.dump(la_park_stat, f, indent=2, sort_keys=True)

    df = pd.read_json('la_park_stat.json')
    df.to_csv('la_park_stat.csv')
    '''
if __name__ == "__main__":
    main()    
