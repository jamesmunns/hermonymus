#!/bin/bash

set -eux

git clone /git /hermonymus

cp /hermonymus/docker/server_crontab /etc/cron.d/scrapecron
chmod 644 /etc/cron.d/scrapecron
/usr/bin/crontab /etc/cron.d/scrapecron

env > /.cronprofile

service cron restart

cd hermonymus/docker

# Run one scrape, in case its a while until the next cronjob
./scrape.sh &

./serve.sh
