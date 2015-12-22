#!/bin/bash
# trap 'kill $(jobs -p)' EXIT  # to be able to quit from electron
source python.env/bin/activate
python api.py
