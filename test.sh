#!/bin/bash

pip3 install requirement.txt
if ! curl -I http://localhost:80/login 2>&1 | grep 200 ; then
    echo "Grafana instance is NOT up."
    exit 1
fi

for i in {1..20}
do
    python3 client.py
    sleep 0.5
done