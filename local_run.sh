#!/bin/bash

#Change directory to the script directory and store the current working directory for later
cwd=$(pwd)
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#Activate virtual environment
source venv/bin/activate

#Run the application
python3 main.py

#Deactivate virtual environment
deactivate

#Change directory back to the original working directory
cd $cwd
