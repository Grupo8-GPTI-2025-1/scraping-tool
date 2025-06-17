
import os
from dotenv import load_dotenv
import requests
import json
from scraper import AirbnbScraper, PortalInmobiliarioScraper

def read_txt(path:str = "input_file.txt"):
    with open(path, "r", encoding="utf-8") as f:
        lineas = [linea.strip() for linea in f]
    return lineas


def post_data(data, bdd_url):
    bdd_url = 'http://localhost:4000/properties'
    headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
    }
    data = [{
        "name": "string",
        "description": "string",
        "property_type": "string",
        "rooms": 0,
        "toilets": 0,
        "location": "string",
        "price": 0,
        "url": "string"
    }]
    response = requests.post(bdd_url, headers=headers, json=data)
    print("POST status:", response.status_code)
    print("POST response:", response.json())

def format_data(data: dict, extras: bool=False):
    formatted_data = {    
        "name": data.get("name", "desconocido"),
        "property_type": data.get("type", "desconocido"),
        "rooms": data.get("rooms", -1),
        "toilets": data.get("bathrooms", -1),
        "price": data.get("price", -1),
        "url": data.get("rooms", -1)
    }
    if extras:
        extra_data = {
            "description": data.get("description", ""),
            "guests": data.get("guests", -1),
            "location": data.get("location", "sin informacion"),
            "nights": data.get("price", -1)
        } 
        formatted_data.update(extra_data)
    return formatted_data

def get_single_data(link):
    if 'https://www.airbnb.cl/' in link:
        print('oferta de airbnb')
        scraper = AirbnbScraper()
        data = scraper.get_data(link)
        scraper.close()
        return [data]
    elif 'https://www.portalinmobiliario.com/' in link:
        print('oferta de portalinmobiliario')
        scraper = PortalInmobiliarioScraper()
        data = scraper.get_data(link)
        scraper.close()
        return [data]
    else:
        print('formato incorrecto')
        return {}
    

def get_data_portal(links: list):
    scraper = PortalInmobiliarioScraper()
    ofertas = list()
    for link in links:
        try:
            data = scraper.get_data(link)
            ofertas.append(format_data(data, False))
        except Exception as e:
            print('Error', e)
    scraper.close()
    return ofertas

def get_data_airbnb(links: list):
    scraper = AirbnbScraper()
    ofertas = list()
    for link in links:
        try:
            data = scraper.get_data(link)
            ofertas.append(format_data(data, True))
        except Exception as e:
            print('Error', e)
    scraper.close()
    return ofertas
    
    
def get_n_post_data(links: list, bdd_url: str):
    ofertas_pi = [link for link in links if 'https://www.portalinmobiliario.com/' in link]
    ofertas_bnb = [link for link in links if 'https://www.airbnb.cl/' in link]
    if len(ofertas_pi) > 0:
        data_pi = get_data_portal(ofertas_pi)
        bdd_url_pi = bdd_url + 'properties'
        print(bdd_url_pi, data_pi)
        # post_data(data_pi, bdd_url_pi)

    if len(ofertas_bnb) > 0:
        data_bnb = get_data_airbnb(ofertas_bnb)
        bdd_url_bnb = bdd_url + 'airbnbs'
        print(bdd_url_bnb, data_bnb)
        # post_data(data_bnb, bdd_url_bnb)






    

if __name__ == '__main__':
    load_dotenv()
    url = os.getenv("API_URL")
    print(f"{url}")
    input_links = read_txt()
    get_n_post_data(links=input_links, bdd_url=url)


    