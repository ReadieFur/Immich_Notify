# Immich Notify
This Python script checks Immich albums for added items and sends notifications via MQTT.

# Setup
Clone this repository and build the docker image.
```bash
git clone
cd immich_notify
docker build -t immich_notify .
```

Out of the box this script is configured to send new files to an MQTT topic.

You can modify the `callback.py` file to change what runs when new content is found. If you want to make major changes to the script (e.g. requiring additional python modules), you will need to rebuild the docker image with an updated `requirements.txt` file (note that when rebuilding a docker image, be sure to remove the old one as this does not happen automatically).

## .env
```
IMMICH_KEY=YOUR_IMMICH_API_KEY
IMMICH_URL=https://immich.domain.com
ALBUMS=["album1", "album2"] (optional)

MQTT_BROKER=YOUR_MQTT_BROKER
MQTT_PORT=YOUR_MQTT_PORT (optional)
MQTT_USER=YOUR_MQTT_USER (optional)
MQTT_PASSWORD=YOUR_MQTT_PASSWORD (optional)
MQTT_TOPIC=YOUR_MQTT_TOPIC (optional)
```

## Docker
```bash
docker run -rm \
  --env-file=.env \
  --volume=./callback.py:/app/callback.py \
  --volume=./cache.json:/app/cache.json \
  immich_notify
```

If you would like to run this script on an interval (e.g. every 5 minutes), I reccoment setting up a cron job. You can do this by running `crontab -e` in your terminal and adding the following line to the file:
```
*/5 * * * * docker run -rm --env-file=/path/to/.env --volume=/path/to/callback.py:/app/callback.py --volume=/path/to/cache.json:/app/cache.json immich_notify
```
