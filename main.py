import os
import ast
import socket
import requests
from urllib.parse import urlparse

IMMICH_KEY = os.environ.get('IMMICH_KEY')
IMMICH_INTERNAL_URL = os.environ.get('IMMICH_INTERNAL_URL')
IMMICH_EXTERNAL_URL = os.environ.get('IMMICH_URL') or IMMICH_INTERNAL_URL
CACHE_PATH = os.environ.get('CACHE_PATH')
ALBUMS = ast.literal_eval(os.environ['ALBUMS'])
DEBUG = (os.getenv('DEBUG', '0') == '1')
MQTT_BROKER = os.environ.get('MQTT_BROKER')
MQTT_PORT = os.environ.get('MQTT_PORT')
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
MQTT_TOPIC = os.environ.get('MQTT_TOPIC') or 'immich'

if IMMICH_KEY is None:
    raise Exception('IMMICH_KEY environment variable not set')
if IMMICH_INTERNAL_URL is None:
    raise Exception('IMMICH_INTERNAL_URL environment variable not set')
if MQTT_BROKER is None:
    raise Exception('MQTT_BROKER environment variable not set')

def check(host, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except:
        return False
    else:
        sock.close()
        return True


def save_data(file_path, dictionary):
    try:
        with open(file_path, 'w') as file:
            for key in dictionary:
                file.write(str(dictionary[key]['total_items']) + '\n')
        if DEBUG:
            print("Data stored successfully!")
    except IOError as error:
        print(error)
        print("An error occurred while saving the file.")


def read_data(file_path):
    tmp = []
    try:
        with open(file_path, 'r') as file:
            for string in file:
                tmp.append(int(string.strip()))
        return tmp
    except IOError as error:
        print(error)
        print("An error occurred while loading the file.")


def get_album_contents(uuid, imkey):
    url = IMMICH_INTERNAL_URL + "/api/album/" + uuid

    payload = {}
    headers = {
        'Accept': 'application/json',
        'x-api-key': imkey
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    a = response.json()

    album_name = a['albumName']
    count = a['assetCount']

    return album_name, count


def ntfy_notification(ntfyurl, ntfytitle, ntfymessage, ntfylink, authorization=''):
    if authorization != '':
        requests.post(ntfyurl,
                      data=ntfymessage.encode('utf-8'),
                      headers={
                          "Title": ntfytitle,
                          "Click": ntfylink,
                          "Icon": NTFY_ICON,
                          "Authorization": "Basic " + authorization
                      })
    else:
        requests.post(ntfyurl,
                      data=ntfymessage.encode('utf-8'),
                      headers={
                          "Title": ntfytitle,
                          "Click": ntfylink,
                          "Icon": NTFY_ICON
                      })


def ntfy_email(ntfyurl, ntfymessage, ntfyemail, ntfytag, authorization=''):
    if authorization != '':
        requests.post(ntfyurl,
                      data=ntfymessage,
                      headers={
                          "Email": ntfyemail,
                          "Tags": ntfytag,
                          "Authorization": "Basic " + authorization
                      })
    else:
        requests.post(ntfyurl,
                      data=ntfymessage,
                      headers={
                          "Email": ntfyemail,
                          "Tags": ntfytag
                      })


if __name__ == '__main__':

    total_items_stored = []
    albums = {}

    url = urlparse(IMMICH_INTERNAL_URL)

    if check(url.hostname, url.port):
        if os.path.exists(CACHE_PATH):
            if DEBUG:
                print('Cache file exists')
            total_items_stored = read_data(CACHE_PATH)
            if DEBUG:
                for item in total_items_stored:
                    print('Items:', item)

            i = 0
            for key in ALBUMS:
                topic = ALBUMS[key]
                if DEBUG:
                    print("Topic: ", topic)
                    print("Album ID: ", key)
                tmp_title, tmp_total = get_album_contents(key, IMMICH_KEY)
                if i < len(total_items_stored):
                    albums[key] = {'topic': topic, 'title': tmp_title, 'total_items': tmp_total,
                                     'stored_items': total_items_stored[i]}
                else:
                    albums[key] = {'topic': topic, 'title': tmp_title, 'total_items': tmp_total,
                                     'stored_items': tmp_total}
                i += 1

            if DEBUG:
                for key in albums:
                    print('Album Name: ', albums[key]['title'])
                    print('Total Items Stored: ', albums[key]['stored_items'])
                    print('Total Items Now: ', albums[key]['total_items'])

            i = 0
            for key in albums:
                albums[key]['new_items'] = albums[key]['total_items'] - albums[key]['stored_items']
                i += 1

            if DEBUG:
                for key in albums:
                    print('Album Name:', albums[key]['title'])
                    print("Items Added:", albums[key]['new_items'])

            for key in albums:
                if albums[key]['new_items'] > 0:
                    topic = albums[key]['topic']
                    url = NTFY_URL + '/' + topic
                    title = 'Immich'
                    link = IMMICH_EXTERNAL_URL + '/albums/' + key

                    if albums[key]['new_items'] > 1:
                        message = str(albums[key]['new_items']) + ' photos added to ' + albums[key]['title'] + '!'
                    else:
                        message = 'Photo added to ' + albums[key]['title'] + '!'

                    ntfy_notification(url, title, message, link, AUTHORIZATION_KEY)

                    if EMAIL != '':
                        topic = albums[key]['topic'] + '_email'
                        url = NTFY_URL + '/' + topic
                        message = 'Immich - ' + message + ' ' + link

                        ntfy_email(url, message, EMAIL, TAG, AUTHORIZATION_KEY)

        else:
            for key in ALBUMS:
                key = key
                topic = ALBUMS[key]
                tmp_title, tmp_total = get_album_contents(key, IMMICH_KEY)
                albums[key] = {'topic': topic, 'title': tmp_title, 'total_items': tmp_total}

            if DEBUG:
                for key in albums:
                    print('Album Name:', albums[key]['title'])
                    print('Total Items Now: ', albums[key]['total_items'])

        save_data(CACHE_PATH, albums)
