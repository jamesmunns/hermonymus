#!/bin/bash

set -eux

python3 /hermonymus/scraper/hermonymus.py \
    -a $API_KEY \
    -m /hermonymus/server/static/site.html \
    --users /cache/users.json \
    --channels /cache/channels.json \
    --history /cache/history.json
