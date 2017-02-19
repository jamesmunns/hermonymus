#!/bin/bash

set -eux

# Required for flask to be happy
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Move "users.py" to a mapped directory
export PYTHONPATH=/auth:PYTHONPATH 

# This is our app!
export FLASK_APP=/hermonymus/server/herm_server.py

# Probably shouldn't use flask to serve, but whatever.
flask run --host=0.0.0.0 --port=80
