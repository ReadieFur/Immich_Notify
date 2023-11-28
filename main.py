import ast
import os
import requests
import json
from dotenv import load_dotenv

DEBUG = os.environ.get('DEBUG') == "true"

if os.environ.get("SKIP_ENV") != "true" and os.path.isfile('.env'):
    load_dotenv()

if not DEBUG:
    if not os.path.isfile('callback.py'):
        raise Exception("No callback.py file found.")
    import callback

IMMICH_KEY = os.environ.get('IMMICH_KEY')
IMMICH_URL = os.environ.get('IMMICH_URL')
ALBUMS = ast.literal_eval(os.environ.get('ALBUMS')) if os.environ.get('ALBUMS') is not None else None
CACHE_FILE = "./cache.json"

if DEBUG:
    import test

def album_api(album_id: str = ''):
    return requests.request("GET", f"{IMMICH_URL}/api/album/{album_id}", headers={
        'Accept': 'application/json',
        'x-api-key': IMMICH_KEY
    }).json()

if __name__ == '__main__':
    cache = json.load(open(CACHE_FILE, 'r')) if os.path.isfile(CACHE_FILE) else {}

    for album in album_api():
        #Query all albums if no albums are specified otherwise only query the specified albums.
        #Only query albums where the number of assets don't match.
        if (ALBUMS is None or album['albumName'] in ALBUMS or album['id'] in ALBUMS) and \
            (album['id'] in cache and len(cache[album['id']]) != album['assetCount']):
            continue

        album = album_api(album['id']) #Get the full album data.
        online_assets = [asset['id'] for asset in album['assets']]
        cached_assets = cache[album['id']] if album['id'] in cache else []
        new_assets = [asset for asset in online_assets if asset not in cached_assets] #Get the difference.
        if len(new_assets) == 0: #This can occur if items are removed.
            continue

        if DEBUG:
            #If debug mode is enabled, use the test.py file instead of callback.py.
            #Additionally, limit the number of messages sent to 5.
            test.album_updated(album, new_assets[:5])
        else:
            callback.album_updated(album, new_assets)

        cache[album['id']] = online_assets

    if os.environ.get('NO_CACHE') != "true":
        with open(CACHE_FILE, 'w') as file:
            json.dump(cache, file)
