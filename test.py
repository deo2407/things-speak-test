import requests
import time
import random

RUSE_LAT = 43.85
RUSE_LON = 25.97
LINK = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={RUSE_LAT}&lon={RUSE_LON}'

WRITE_API_KEY = 'FTOBS0765E4VGFNM'
SLEEP_TIME = 20


def get_data():
    headers = {'User-Agent': 'deo'}
    r = requests.get(LINK, headers=headers)
    res = r.json()

    temperature = res['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']
    relative_humidity = res['properties']['timeseries'][0]['data']['instant']['details']['relative_humidity']

    return temperature, relative_humidity


def send_data(temperature, relative_humidity):
    url = 'https://api.thingspeak.com/channels/2044962/bulk_update.json'

    json_data = {
        "write_api_key": WRITE_API_KEY,
        "updates": [{
            "delta_t": SLEEP_TIME,
            "field1": temperature,
            "field2": relative_humidity,
            "field3": random.randrange(0, 10000)
        }]
    }

    r = requests.post(url, json=json_data)
    print(r.text)


while True:
    temperature, relative_humidity = get_data()

    print(get_data())

    send_data(temperature, relative_humidity)

    time.sleep(SLEEP_TIME)
