import os
import json
import paho.mqtt.publish as mqtt

MQTT_BROKER = os.environ.get('MQTT_BROKER')
MQTT_PORT = int(os.environ.get('MQTT_PORT')) if os.environ.get('MQTT_PORT') is not None else 1883
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
MQTT_TOPIC = os.environ.get('MQTT_TOPIC') or 'immich'

def album_updated(album, new_assets: list[str]):
    print(f"{len(new_assets)} new assets found in '{album['albumName']}'")
    mqtt.single(
        topic=f"{MQTT_TOPIC}/{album['id']}",
        payload=json.dumps(new_assets),
        hostname=MQTT_BROKER,
        port=MQTT_PORT,
        auth={"username": MQTT_USERNAME, "password": MQTT_PASSWORD} if MQTT_USERNAME is not None else None
    )
