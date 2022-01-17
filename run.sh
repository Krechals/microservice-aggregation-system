#!/bin/bash

if [ -z "${SPRC_DVP}" ]; then
    echo 'Environment variable SPRC_DVP is not set.'
    echo 'Example: export SPRC_DVP=/var/lib/docker/volumes'
    exit 1
fi

docker-compose -f stack.yml build
docker stack deploy -c stack.yml sprc3