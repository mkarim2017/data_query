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

def get_ca_museums():
    URL = "https://en.wikipedia.org/wiki/List_of_museums_in_California"
    page = requests.get(URL)
    # print(page.text)
    soup = BeautifulSoup(page.text, "html.parser")

    list = soup.find("table", class_="wikitable sortable").find("tbody").find_all("tr")
    list = list[1:]
    museums = []

    for l in list:
        try:
            m = {}
            m["Name"] = {}
            m["Town/City"] = {}
            m["County"] = {}
            m["Region"] = {}
            m["Type"] = {}
            m["Summary"] = {}
            href = urljoin("https://en.wikipedia.org/", l.find_all('a')[0].get('href'))
            lat_lon = get_location(href)
            try:
                m["latitude"] = lat_lon.split(';')[0].strip()
            except Exception:
                m["latitude"] = ""
            try:
                m["longitude"] = lat_lon.split(';')[1].strip()
            except Exception:
                 m["longitude"] = ""

         
            try:
                m["Town/City"] = l.find_all('td')[1].text.strip()
                m["County"] = l.find_all('td')[2].text.strip()
                m["Region"] = l.find_all('td')[3].text.strip()
                m["Type"] = l.find_all('td')[4].text.strip()
                m["Summary"] = l.find_all('td')[5].text.strip()
            except Exception as err:
                print(str(err))
            m["href"] = href
            print(json.dumps(m, indent=2))
            museums.append(m)           
        except Exception as err:
            print(str(err))

    with open("CA_Museums.json", "w") as f:
        json.dump(museums, f, indent=2, sort_keys=False)

    df = pd.read_json('CA_Museums.json')
    df.to_csv('CA_Museums.csv')


def get_county_museums(county="LA", URL="https://en.wikipedia.org/wiki/List_of_museums_in_Los_Angeles_County,_California"):
    page = requests.get(URL)
    # print(page.text)
    soup = BeautifulSoup(page.text, "html.parser")

    list = soup.find("table", class_="wikitable sortable").find("tbody").find_all("tr")
    header = list[0]
    column_list = [l.text.strip() for l in header.find_all('td')]
    print(column_list)
    list = list[1:]
    museums = []

    for l in list:
        try:
            m = {}
            m["Name"] = l.find_all('a')[0].text.strip()
            print(m["Name"])
            href = urljoin("https://en.wikipedia.org/", l.find_all('a')[0].get('href'))
            
            lat_lon = get_location(href)
            try:
                m["latitude"] = lat_lon.split(';')[0].strip()
            except Exception:
                m["latitude"] = ""
            try:
                m["longitude"] = lat_lon.split(';')[1].strip()
            except Exception:
                 m["longitude"] = ""
            try:
                m["Town/City"] = l.find_all('td')[1].text.strip()
                m["County"] = l.find_all('td')[2].text.strip()
                if "Region" in column_list:
                    m["Region"] = l.find_all('td')[3].text.strip()
                    m["Type"] = l.find_all('td')[4].text.strip()
                    m["Summary"] = l.find_all('td')[5].text.strip()
                else:
                    m["Type"] = l.find_all('td')[3].text.strip()
                    m["Summary"] = l.find_all('td')[4].text.strip()
            except Exception as err:
                print(str(err))

            m["href"] = href
            print(json.dumps(m, indent=2))
            museums.append(m)
        except Exception as err:
            print(str(err))

    json_file = "{}_County_Museums.json".format(county)
    csv_file = "{}_County_Museums.csv".format(county)

    with open(json_file, "w") as f:
        json.dump(museums, f, indent=2, sort_keys=False)

    df = pd.read_json(json_file)
    df.to_csv(csv_file)


def get_beach_details(URL):
    activities = ""
    facilities = ""
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    if "lacounty" in URL:
        print("get_beach_details")
        list = soup.find_all('div', class_="grve-box-title grve-h3")
        print(list)

def get_la_county_beaches():
    URL = "https://www.laalmanac.com/parks/pa11.php"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    content = soup.find('div', class_="content-box")
    list = content.find('table').find('tbody').find_all('tr')
    # print(list)
    beaches = []

    for l in list:
        try:
            m = {}
            data = l.find_all('td')
            m["Name"] = data[0].text.strip()
            m["Address"] = data[0].text.strip()
            m["Activities"] = ""
            m["Facilities"] = ""
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
            print(json.dumps(m, indent=2))
            beaches.append(m)
        except Exception as err:
            print(str(err))

    with open("LA_County_Beaches.json", "w") as f:
        json.dump(beaches, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_County_Beaches.json')
    df.to_csv('LA_County_Beaches.csv')

def get_la_county_parks_laalmanac():
    URL = "https://www.laalmanac.com/parks/pa10.php"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    content = soup.find('div', class_="content-box")
    list = content.find('table').find('tbody').find_all('tr')
    # print(list)
    parks = []

    for l in list:
        locality = ""
        try:
            m = {}
            data = l.find_all('td')
            i = 0
            if len(data) == 3:
                locality = data[i].text.strip()
                i = i + 1
            m["Name"] = data[i].text.strip()
            i = i+1
            m["Address"] = data[i].text.strip()
            m["Activities"] = ""
            m["Facilities"] = ""
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
            print(json.dumps(m, indent=2))
            parks.append(m)
        except Exception as err:
            print(str(err))

    with open("LA_County_Parks_LAAlmanac.json", "w") as f:
        json.dump(parks, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_County_Parks_LAAlmanac.json')
    df.to_csv('LA_County_Parks_LAAlmanac.csv')

def get_la_museums():
    URL = "https://www.laparks.org/museums"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    content = soup.find_all('div', class_="view-content")[1]
    list = content.find('table').find('tbody').find_all('tr')

    museums = []
    for l in list:
        try:
            m = {}
            m["Name"] = l.find('a').text.strip()
            href = urljoin("https://www.laparks.org/museums", l.find('a').get('href'))
            m["Address"] = l.find('td', class_="views-field-field-address").text.strip()
            lat=""
            lon=""
            try:
                lat, lon = get_lat_lon_from_address(m["Address"])
            except Exception as err:
                print(str(err))
            m["lat"] = lat
            m["lon"] = lon
            m["href"] = href
            print(json.dumps(m, indent=2))
            museums.append(m)
        except Exception as err:
            print(str(err))

    with open("LA_Museums.json", "w") as f:
        json.dump(museums, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_Museums.json')
    df.to_csv('LA_Museums.csv')
           
    

def get_park_details(href):
    base_url = "https://www.laparks.org"
    URL = urljoin(base_url, href)
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    # print(page.text)
    details = {}
    facilities = ""
    address = ""
    try:
        labels = soup.find_all('div', class_="field-label")
        for l in labels:
            if "Facility Features" in l.text.strip():
                facilities = l.find_next_siblings("div")[0].text.strip()
    except Exception as err:
        print(str(err))

    try:
        address = soup.find_all('div', class_="field-name-field-address")[0].text.strip()
        if "Address:" in address:
            address = address.split("Address:")[1].strip()
        print("ADDRESS : {}".format(address))
    except Exception as err:
        print(str(err))
        

    details["facilities"] = facilities
    details["address"] = address    
    return details


def get_parks_la_county():
    URL = "view-source:https://parks.lacounty.gov/park-overview/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    la_parks = []
    print(soup)
    parks = soup.find("div", {"id": "popmake-23003"})
    parks = soup.find_all('div', class_="floating-menu")
    print(parks)
    return
    parks = soup.find_all("tbody")[0].find_all('tr')
    for p in parks:
        c_p = {}
        href = p.find_all('a')[0].get("href")
        details = get_park_details(href)

        c_p["Park Name"] = p.find_all('a')[0].text.strip()
        # print(c_p["p_name"])
        if len(details["address"]) > 0:
            c_p["Address"] = details["address"]
        else:
            c_p["Address"] = p.find_all('td')[1].text.strip()
        lat=""
        lon=""
        try:
            lat, lon = get_lat_lon_from_address(c_p["Address"])
        except Exception as err:
            print(str(err))
        c_p["latitude"] = lat
        c_p["longitude"] = lon

        # print(c_p["p_address"])
        c_p["Facility Features"] = details["facilities"]

        la_parks.append(c_p)


    with open("LA_Parks.json", "w") as f:
        json.dump(la_parks, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_Parks.json')
    df.to_csv('LA_Parks.csv')


def get_municipal_parks_la_city2():
    URL = "https://en.wikipedia.org/wiki/List_of_parks_in_Los_Angeles"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    la_municipal_parks = []
    list = soup.find_all("table", class_="wikitable")[1].find("tbody").find_all("tr")
    list = list[1:]

    for l in list:
        print(l)
        m = {}
        try:
            m["Name"] = l.find_all('td')[0].text.strip()
            m["Location"] = l.find_all('td')[1].text.strip()
            href = urljoin("https://en.wikipedia.org/", l.find_all('a')[0].get('href'))

            if "latitude" in m["Location"]:
                try:
                    m["Location"] = m["Location"].splt('<')[0]
                    lat_lon = get_location(href)
                    m["latitude"] = lat_lon.split(';')[0].strip()
                    m["longitude"] = lat_lon.split(';')[1].strip()
                except Exception:
                    m["latitude"] = ""
                    m["longitude"] = ""
            else:
                try:
                    m["latitude"], m["longitude"] = get_lat_lon_from_address(m["Location"])
                except Exception:
                    m["latitude"] = ""
                    m["longitude"] = ""

            m["href"] = href
            print(json.dumps(m, indent=2))
           
        except Exception as err:
            print(str(err))

        la_municipal_parks.append(m)

    with open("CA_MUNICIPAL_PARKS.json", "w") as f:
        json.dump(la_municipal_parks, f, indent=2, sort_keys=False)

    df = pd.read_json('CA_MUNICIPAL_PARKS.json')
    df.to_csv('CA_MUNICIPAL_PARKS.csv')

def get_state_parks_la_city2():
    URL = "https://en.wikipedia.org/wiki/List_of_parks_in_Los_Angeles"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    la_state_parks = []
    list = soup.find("table", class_="wikitable sortable").find("tbody").find_all("tr")
    list = list[2:]

    for l in list:
        try:
            m = {}
            m["Name"] = {}
            m["Classification"] = {}
            m["Location"] = {}
            
            # m["Region"] = {}
            # m["Type"] = {}
            m["Summary"] = {}
            href = urljoin("https://en.wikipedia.org/", l.find_all('a')[0].get('href'))
            lat_lon = get_location(href)
            try:
                m["latitude"] = lat_lon.split(';')[0].strip()
            except Exception:
                m["latitude"] = ""
            try:
                m["longitude"] = lat_lon.split(';')[1].strip()
            except Exception:
                 m["longitude"] = ""


            try:
                m["Name"] = l.find_all('td')[0].text.strip()
                m["Classification"] = l.find_all('td')[1].text.strip()
                m["Location"] = l.find_all('td')[2].text.strip().encode("ascii", "ignore").decode()
                # m["Type"] = l.find_all('td')[3].text.strip()
                m["Summary"] = l.find_all('td')[6].text.strip()
            except Exception as err:
                print(str(err))
            m["href"] = href
            print(json.dumps(m, indent=2))
           
        except Exception as err:
            print(str(err))

        la_state_parks.append(m)

    with open("CA_STATE_PARKS.json", "w") as f:
        json.dump(la_state_parks, f, indent=2, sort_keys=False)

    df = pd.read_json('CA_STATE_PARKS.json')
    df.to_csv('CA_STATE_PARKS.csv')


def get_state_parks_la_county():
    URL = "https://en.wikipedia.org/wiki/List_of_parks_in_Los_Angeles_County,_California"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    la_state_parks = []
    list = soup.find("table", class_="wikitable sortable").find("tbody").find_all("tr")
    list = list[2:]

    for l in list:
        try:
            m = {}
            m["Name"] = {}
            m["Classification"] = {}
            m["Location"] = {}
            
            # m["Region"] = {}
            # m["Type"] = {}
            m["Summary"] = {}
            href = urljoin("https://en.wikipedia.org/", l.find_all('a')[0].get('href'))
            lat_lon = get_location(href)
            try:
                m["latitude"] = lat_lon.split(';')[0].strip()
            except Exception:
                m["latitude"] = ""
            try:
                m["longitude"] = lat_lon.split(';')[1].strip()
            except Exception:
                 m["longitude"] = ""


            try:
                m["Name"] = l.find_all('td')[0].text.strip()
                m["Classification"] = l.find_all('td')[1].text.strip()
                m["Location"] = l.find_all('td')[2].text.strip().encode("ascii", "ignore").decode()
                # m["Type"] = l.find_all('td')[3].text.strip()
                m["Summary"] = l.find_all('td')[6].text.strip()
            except Exception as err:
                print(str(err))
            m["href"] = href
            print(json.dumps(m, indent=2))
           
        except Exception as err:
            print(str(err))

        la_state_parks.append(m)

    with open("LA_COUNTY_STATE_PARKS.json", "w") as f:
        json.dump(la_state_parks, f, indent=2, sort_keys=False)

    df = pd.read_json('LA_COUNTY_STATE_PARKS.json')
    df.to_csv('LA_COUNTY_STATE_PARKS.csv')

def get_parks_la_city():
    URL = "https://www.laparks.org/parks"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    la_parks = []
    parks = soup.find_all("tbody")[0].find_all('tr')
    for p in parks:
        c_p = {}
        href = p.find_all('a')[0].get("href")
        details = get_park_details(href)

        c_p["Park Name"] = p.find_all('a')[0].text.strip()
        # print(c_p["p_name"])
        if len(details["address"]) > 0:
            c_p["Address"] = details["address"]
        else:
            c_p["Address"] = p.find_all('td')[1].text.strip()
        lat=""
        lon=""
        try:
            lat, lon = get_lat_lon_from_address(c_p["Address"])
        except Exception as err:
            print(str(err))
        c_p["latitude"] = lat
        c_p["longitude"] = lon

        # print(c_p["p_address"])
        c_p["Facility Features"] = details["facilities"]

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
    get_la_county_parks_laalmanac()
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
