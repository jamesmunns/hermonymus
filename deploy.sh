#!/bin/bash

set -eux

git push -f droplet master

ssh droplet ' \
    cd hosting/hermonymus && \
    git reset --hard master && \
    cd docker && \
    docker build -t hermonymus . && \
    docker stop james_herm ||:; \
    docker rm james_herm ||:; \
    docker run \
        --name james_herm \
        --env-file secrets/api.keys \
        -v $(pwd)/cache:/cache \
        -v $(pwd)/..:/git:ro \
        -v $(pwd)/secrets:/auth:ro \
        -d hermonymus'
