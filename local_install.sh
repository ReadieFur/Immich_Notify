#!/bin/bash
git clone https://github.com/ReadieFur/Immich_Notify.git
cd immich_notify
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
chmod +x local_run.sh
