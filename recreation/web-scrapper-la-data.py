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

def get_park_details(href):
    base_url = "https://www.laparks.org"
    URL = urljoin(base_url, href)
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    # print(page.text)
    facilities = ""
    try:
        labels = soup.find_all('div', class_="field-label")
        for l in labels:
            if "Facility Features" in l.text.strip():
                facilities = l.find_next_siblings("div")[0].text.strip()
    except Exception as err:
        print(str(err))

    return facilities

def get_parks_la():
    URL = "https://www.laparks.org/parks"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    la_parks = []
    parks = soup.find_all("tbody")[0].find_all('tr')
    for p in parks:
        c_p = {}
        href = p.find_all('a')[0].get("href")
        # print(href)
        c_p["Park Name"] = p.find_all('a')[0].text.strip()
        # print(c_p["p_name"])
        c_p["Address"] = p.find_all('td')[1].text.strip()
        # print(c_p["p_address"])
        c_p["Facility Features"] = get_park_details(href)
        la_parks.append(c_p)
        

    with open("LA_Parks.json", "w") as f:
        json.dump(la_parks, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_Parks.json')
    df.to_csv('LA_Parks.csv') 
        
        
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
               
            
def get_city_courses(url, course_list):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    results = soup.find_all('div', class_="resultContainer")

    courses = []
    for r in results:

        try:
            rh = r.find('div', class_="resultsHeader")
            c_name = rh.find('a').text.strip()
            href = urljoin("https://www.golflink.com/golf-courses", rh.find('a').get('href'))

            if c_name in course_list:
                continue

            print(c_name)
            course_list.append(c_name)
            c_c = {}
            c_c["Name"] = c_name 
            c_c["href"] = href

            tc = r.find('div', class_="textcontainer")
            infos =[x.strip() for x in tc.text.strip().split("\n")]
            infos = [ i for i in infos if i]
            data = ", ".join(infos).strip().split("Write a Review")
            info = data[0].strip()
            address = ""
            try:
                address = data[1].split("Check Tee Times,")[1].split('.')[0].strip()
            except Exception as err:
                print(str(err))
                print(data[1])
                address = data[1].strip().replace("Check Tee Times,", "").replace("Check Tee Times", "")
            address = address.split("(")[0].rstrip(", ").strip()  
            address = address.replace("\u00a0", " ").lstrip(",").strip()
            lat = ""
            lon = ""
            try:
                lat, lon = get_lat_lon_from_address(address)
            except Exception as err:
                print(str(err))
            c_c["address"] = address
            c_c["latitude"] = lat
            c_c["longitude"] = lon
            c_c["info"] = info
            print(json.dumps(c_c, indent=2))
            courses.append(c_c)
        except Exception as err:
            print(str(err))

    return courses, course_list

def get_golf_courses():
    URL = "https://www.golflink.com/golf-courses/ca/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    lists = soup.find_all('ul', class_="bullet2 golf_courses links_2colA sList")

    course_list = []
    courses = []
    city_list = []
    for list in lists:
        ls = list.find_all('li')
        for l in ls:
            city = l.text.strip()
            href = urljoin("https://www.golflink.com/golf-courses", l.find('a').get('href'))
            if city not in city_list:
                try:
                    city_list.append(city)
                    city_courses, course_list  = get_city_courses(href, course_list)
                    courses.extend(city_courses)
                except Exception as err:
                    print(str(err))    

    
    with open("CA_GOLF_COURSES.json", "w") as f:
        json.dump(courses, f, indent=2, sort_keys=False)

    df = pd.read_json('CA_GOLF_COURSES.json')
    df.to_csv('CA_GOLF_COURSES.csv')



def get_city_data(city, state="california"):

    city_data = {}
    city_data["Name"] = city
    city_data["city_id"] = "N/A"
    city_data["No of Parks"] = "N/A"
    city_data["percent residents live within a 10 minute walk of a park"] = "N/A"
    city_data["city_id"] = "N/A"

    try:
        URL = "https://www.tpl.org/city/{}-{}".format(city.replace(' ', '-').lower(), state.lower())
        print(URL)
        page = requests.get(URL)
        if page.status_code != 200:
            sleep(10)
            page = requests.get(URL)

        soup = BeautifulSoup(page.text, "html.parser")

        try:
            city_data["percent residents live within a 10 minute walk of a park"] = soup.find("div", class_="city-rank").text.split("%")[0].strip()
        except Exception as err:
            print("{} 10 m: {}".format(city, str(err)))

        try:
            text_ct = soup.find('div', class_="info-container").find('div', class_="text-container")
            city_data["No of Parks"] = text_ct.find('div', class_="heading").text.split("Has")[1].split("Parks")[0].strip()
        except Exception as err:
            print("{} text_ct: {}".format(city, str(err)))

        try:
            graph_ct = soup.find('div', class_="percent-land-use-graph-section").find('div', class_="graph-intro-container")
            city_data["Percent city land is used for parks and recreation"] = graph_ct.text.split("%")[0].strip()
        except Exception as err:
            print("{} graph_ct: {}".format(city, str(err)))
        try:
            city_data["city_id"] = text_ct.find_all('a')[0].get('href').split("CityID=")[1].strip()
        except Exception as err:
            print("{} : {}".format(city, str(err)))
    except Exception as err:
        print("{} city_id : {}".format(city, str(err)))

    print(json.dumps(city_data, indent=2))
    return city_data

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

    #get_parks_la()
    #get_water_resources()
    get_golf_courses()
    #get_city_data('Yorba Linda')

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
