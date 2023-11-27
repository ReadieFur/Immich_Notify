#!/bin/bash

#Change directory to the script directory and store the current working directory for later
cwd=$(pwd)
cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

#Activate virtual environment
source venv/bin/activate

#Load the environment variables
#https://gist.github.com/mihow/9c7f559807069a03e302605691f85572
if [ ! -f .env ]
then
  export $(cat .env | xargs)
fi

#Run the application
python3 main.py

#Deactivate virtual environment
deactivate

#Change directory back to the original working directory
cd $cwd
