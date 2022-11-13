import requests
from lxml import html
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
from time import sleep
import os

def get_sc_la():
    s_centers = []
    URL = "https://www.laparks.org/scc"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")
    centers = soup.find_all("table")[0].find('tbody').find_all('tr')
    # print(centers)
    for sc in centers:
        s_c = {}
        data = sc.find_all('td')
        link = "{}{}".format("https://www.laparks.org", data[0].find('a').get('href'))
        s_c["Name"] = data[0].find('a').text.strip()
        s_c["Address"] = data[1].text.strip()
        # print("{} : {} : {}".format(name, address, link))
        page2 = requests.get(link)
        soup2 = BeautifulSoup(page2.text, "html.parser")
        s_c["Facility-Features"] = "NA"
        s_c["Sports-Fitness-Programs"] = "NA"
        s_c["Cultural-Programs"] = "NA"
        print(json.dumps(s_c, indent=2))
    
        '''
        for lab in soup2.select("field-label"):
            print(lab.text)
            print(lab.find_next_sibling().text)

        '''


        # print(page2.text)
        rows = soup2.find_all('div', class_="row")

        for row in rows:
            try:
                
                label = row.find('div', class_="field-label").text.strip()
                items = row.find('div', class_="field-items").text.strip()
                if label == "Sports and Fitness Programs":
                    s_c["Sports-Fitness-Programs"] = items
                elif label == "Cultural Programs":
                    s_c["Cultural-Programs"] = items
                elif label == "Facility Features":
                    s_c["Facility-Features"] = items
            except Exception as err:
                pass
        print(json.dumps(s_c, indent=2))
        s_centers.append(s_c)

    with open("LA_SC.json", "w") as f:
        json.dump(s_centers, f, indent=2, sort_keys=True)

    df = pd.read_json('LA_SC.json')
    df.to_csv('LA_SC.csv')

    '''
        #print("activities : {}".format(activities))
        # activities = soup2.find_all('div', class_="col-sm-12")
        # print("activities : {}".format(activities))
        facility_features_label = activities.find('div', class_="field-label").text.strip()
        facility_features_items = activities.find('div', class_="field-items").text.strip()
        print("label : {} : items: {}".format(facility_features_label, facility_features_items))

        activities = soup2.find_all('div', class_="row")[8]
        facility_features_label = activities.find('div', class_="field-label").text.strip()
        facility_features_items = activities.find('div', class_="field-items").text.strip()
        print("label : {} : items: {}".format(facility_features_label, facility_features_items))
        activities = soup2.find_all('div', class_="row")[9]
        facility_features_label = activities.find('div', class_="field-label").text.strip()
        facility_features_items = activities.find('div', class_="field-items").text.strip()
        print("label : {} : items: {}".format(facility_features_label, facility_features_items))
    '''
def get_sc_ca():
    URL = "https://www.careforcalifornia.net/list11_ca_senior_centers.htm"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    s_centers = []
    centers = soup.find_all("table")[4].find_all('tr')
    for sc in centers:
        s_c = {}
        data = sc.find_all('td')
        s_c["Name"] = data[0].text.strip()
        s_c["City"] = data[1].text.strip()
        s_c["County"] = data[2].text.strip()
        s_c["Phone"] = data[3].text.strip()
        print(s_c)
        print(json.dumps(s_c, indent=2))
        s_centers.append(s_c)

    with open("CA_SC.json", "w") as f:
        json.dump(s_centers, f, indent=2, sort_keys=True)

    df = pd.read_json('CA_SC.json')
    df.to_csv('CA_SC.csv') 
        
        

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

    get_sc_la()

    # get_sc_ca()

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
