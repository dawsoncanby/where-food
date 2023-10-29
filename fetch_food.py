import requests
import json


def format_entry(e):
    grab_fields = ['name', 'image_url', 'rating']
    entry = {
        field: e[field] for field in grab_fields
    }
    entry['address'] = ', '.join(e['location']['display_address'])
    entry['categories'] = [c['title'] for c in e['categories']]
    return entry


with open('configs/yelp_api_key.txt') as f:
    api_key = f.read().strip()

offset = 0
chunk_size = 50

businesses = []
while True:
    endpoint = 'https://api.yelp.com/v3/businesses/search'
    params = {
        'location': 'Fort Collins, Colorado',
        'term': 'restaurants',
        'limit': chunk_size,
        'offset': offset
    }
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(endpoint, params=params, headers=headers)
    # we get a 500 or 400 when offset is greater than total locations, just break then
    # TODO: fix
    if response.status_code == 500 or response.status_code == 400:
        break
    response.raise_for_status()
    data = response.json()['businesses']

    formatted = [format_entry(e) for e in data]
    businesses.extend(formatted)

    offset += chunk_size

with open('public/food.json', 'w', encoding='utf-8') as f:
    json.dump(businesses, f, indent=2)
