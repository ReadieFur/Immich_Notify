import ast
import os
import requests
import json
import paho.mqtt.publish as mqtt

IMMICH_KEY = os.environ.get('IMMICH_KEY')
IMMICH_INTERNAL_URL = os.environ.get('IMMICH_INTERNAL_URL')
ALBUMS = ast.literal_eval(os.environ.get('ALBUMS')) if os.environ.get('ALBUMS') is not None else None
CACHE_FILE = os.environ.get('CACHE_FILE')
MQTT_BROKER = os.environ.get('MQTT_BROKER')
MQTT_PORT = int(os.environ.get('MQTT_PORT')) if os.environ.get('MQTT_PORT') is not None else 1883
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
MQTT_TOPIC = os.environ.get('MQTT_TOPIC') or 'immich'

def get_cache() -> dict[str, int]:
    if CACHE_FILE is None or not os.path.isfile(CACHE_FILE):
        return {}
    with open(CACHE_FILE, 'r') as file:
        return json.load(file)

def album_api(album_id: str = ''):
    return requests.request("GET", f"{IMMICH_INTERNAL_URL}/api/album/{album_id}", headers={
        'Accept': 'application/json',
        'x-api-key': IMMICH_KEY
    }).json()

def get_album_contents(album_id: str) -> list[str]:
    """Returns a list of asset UUIDs in the specified album."""
    album = album_api(album_id)
    return [asset['id'] for asset in album['assets']]

def publish_mqtt(album_name: str, new_assets: list[str]):
        mqtt.single(
            topic=f"{MQTT_TOPIC}/{album_name}",
            payload=json.dumps(new_assets),
            hostname=MQTT_BROKER,
            port=MQTT_PORT,
            auth={"username": MQTT_USERNAME, "password": MQTT_PASSWORD} if MQTT_USERNAME is not None else None
        )

if __name__ == '__main__':
    cache = get_cache()

    for album in album_api():
        #Query all albums if no albums are specified otherwise only query the specified albums.
        #Only query albums where the number of assets don't match.
        if (ALBUMS is None or album['albumName'] in ALBUMS or album['id'] in ALBUMS) and \
            (album['id'] in cache and len(cache[album['id']]) != album['assetCount']):
            continue

        online_assets = get_album_contents(album['id'])
        cached_assets = cache[album['id']] if album['id'] in cache else []
        new_assets = [asset for asset in online_assets if asset not in cached_assets] #Get the difference.
        if len(new_assets) == 0: #This can occur if items are removed.
            continue

        print(f"{len(new_assets)} new assets found in '{album['albumName']}'")

        publish_mqtt(album['albumName'], new_assets)

        cache[album['id']] = online_assets

    if CACHE_FILE is not None:
        with open(CACHE_FILE, 'w') as file:
            json.dump(cache, file)
