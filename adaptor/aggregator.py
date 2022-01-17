from influxdb import InfluxDBClient
from datetime import datetime, timezone
from pytz import timezone
import paho.mqtt.client as mqtt
import json
import logging
import os

db_client = InfluxDBClient(host='db-container', 
            port=8086,
            username='root', 
            password='pass',
            database='db0')
db_client.create_database('db0')

def is_int(nr):
    try:
        nr = int(nr)
    except:
        return False
    return True

def is_float(nr):
    try:
        nr = float(nr)
    except:
        return False
    return True

# Callback from messaging broker when connecting.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

# Callback from messaging broker when someone publish on any topic.
def on_message(client, userdata, msg):
    host_param = msg.topic.split('/')
    location = host_param[0]
    station = host_param[1] 
    
    json_obj = json.loads(msg.payload)
    if os.getenv('DEBUG_DATA_FLOW'):
        logging.info(f'Received a message by topic [{msg.topic}]')
        if 'timestamp' in json_obj:
            logging.info(f'Data timestamp is: {json_obj["timestamp"]}')
        else:
            logging.info('Data timestamp is NOW')

    db_elems = []
    for key, value in json_obj.items():
        if is_int(value) or is_float(value):
            if os.getenv('DEBUG_DATA_FLOW'):
                logging.info(f'{msg.topic}.{key} {value}')
            db_elems.append({
                'measurement': f'{station}.{key}',
                'tags': {
                    'location': location,
                    'station': station
                },
                'time': json_obj['timestamp'],
                'fields': {
                    'value': value
                }
            })

    # Add elements to DB in batch.
    db_client.write_points(db_elems)

def broker_connect():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker-container")
    client.loop_forever()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    broker_connect()