# Immich Notify
This Python script checks Immich albums for added items and sends notifications via MQTT.

# Table of Contents
- [Immich Notify](#immich-notify)
- [Table of Contents](#table-of-contents)
- [Installation and Usage](#installation-and-usage)
  - [The Docker Way](#the-docker-way)
    - [Installation](#installation)
    - [.env](#env)
    - [Docker](#docker)
  - [The Local Way](#the-local-way)
    - [Requirements](#requirements)
    - [Installation](#installation-1)
    - [.env](#env-1)
    - [Running](#running)

# Installation and Usage
There are two ways you can setup and use this script. Both are fairly easy to setup and use and each have their own advantages.

## The Docker Way
This option is for installing and running the script in a docker container. This is the easiest way to get up and running.

### Installation
Clone this repository and build the docker image.
```bash
git clone https://github.com/ReadieFur/Immich_Notify.git
cd immich_notify
docker build -t immich_notify .
```

Out of the box this script is configured to send new files to an MQTT topic.

You can modify the `callback.py` file to change what runs when new content is found. If you want to make major changes to the script (e.g. requiring additional python modules), you will need to rebuild the docker image with an updated `requirements.txt` file (note that when rebuilding a docker image, be sure to remove the old one as this does not happen automatically).

### .env
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

### Docker
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

## The Local Way
This option is for installing and running the script locally. This method is preffered if you plan to make major changes to the script.

### Requirements
- Python 3
- pip
- virtualenv
- git

You can install these requirements on Ubuntu by running the following command:
```bash
sudo apt install python3 python3-pip virtualenv git
```

### Installation
Run the following command to automatically install the script and it's Python dependencies in `./immich_notify`.
```bash
curl -s https://raw.githubusercontent.com/ReadieFur/Immich_Notify/master/install.sh | bash
```

The above script will clone this repository and create a virtual environment in `./immich_notify` and install the script and it's Python dependencies.

### .env
Please see the [Docker .env](#env) section above for information on the `.env` file.

### Running
A script is provided to automatically run the script in the virtual environment and load the `.env` file. You can run the script by running the following command:
```bash
./run_local.sh
```

You can also run this script on an interval (e.g. every 5 minutes) by setting up a cron job. You can do this by running `crontab -e` in your terminal and adding the following line to the file:
```
*/5 * * * * /path/to/immich_notify/run_local.sh
```
