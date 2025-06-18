import requests
import json


def post_data(data, bdd_url):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    print("Enviando datos:")
    print(json.dumps(data, indent=2))
    response = requests.post(bdd_url, headers=headers, json=data)
    print("POST status:", response.status_code)
    try:
        print("POST response:", response.json())
    except Exception:
        print("POST response no es JSON válido:")
        print(response.text)

def format_data(data: dict, extras: bool=False):
    formatted_data = {    
        "name": data.get("name", "desconocido"),
        "property_type": data.get("type", "desconocido"),
        "rooms": data.get("rooms", 0),
        "toilets": data.get("bathrooms", 0),
        "price": data.get("price", 0),
        "url": data.get("url", "desconocido"),
        "description": data.get("description", "sin descripcion"),
        "location": data.get("location", "sin informacion"),

    }
    if extras:
        extra_data = {
            "guests": data.get("guests", 1),
            "nights": data.get("nights", 5),
        } 
        formatted_data.update(extra_data)
    return formatted_data