import requests
import json
import os


def get_infos(place, key):
    count = 0
    results = []
    session = requests.session()
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'\
        '?location=21.021942,105.792078'\
        '&radius=2000&'\
        'type={}&key={}'
    page = '&pagetoken={}'
    r = session.get(url.format(place, key))
    data = r.json()
    print(data)
    next_token = data['next_page_token']
    for location in data['results']:
        name = location['name']
        name = location['name']
        lat = location['geometry']['location']['lat']
        lng = location['geometry']['location']['lng']
        address = location['vicinity']
        results.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lng,lat]
                },
                "properties": {
                    "name": name,
                    "address": address
                }
            }
        )
    next_url = url + page
    r = session.get(next_url.format(place, key, next_token))
    data = r.json()
    print(data)
    while count < 5:
        name = data['results'][count]['name']
        name = data['results'][count]['name']
        lat = data['results'][count]['geometry']['location']['lat']
        lng = data['results'][count]['geometry']['location']['lng']
        address = data['results'][count]['vicinity']
        results.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lng,lat]
                },
                "properties": {
                    "name": name,
                    "address": address
                }
            }
        )
        count += 1
    return results


def get_place(key):
    results = []
    results.append(get_infos('bar', key))
    results.append(get_infos('restaurant', key))
    map_data = {
        "type": "FeatureCollection",
        "features": results
    }
    with open('map.geojson', 'wt') as f:
        f.write(json.dumps(map_data, indent=4))

def main():
    token_path = os.path.join(os.path.dirname(__file__), "token.json")
    with open(token_path, "rt") as file:
        key = json.loads(file.read())['key']
    get_place(key)


if __name__ == '__main__':
    main()
