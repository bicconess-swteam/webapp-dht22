#!/bin/sh

export FLASK_APP=run.py
export FLASK_CONFIG=development
export FLASK_RUN_PORT=1234
# source $(pipenv --venv)/bin/activate
# flask run -h 0.0.0.0
python home/pi/Development/tatooine-project/webapp-dht22/run.py
