import paho.mqtt.client as mqtt
import json
from influxdb import InfluxDBClient
from datetime import datetime, timezone
from pytz import timezone

db_client = InfluxDBClient(host='localhost', 
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

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    host_param = msg.topic.split('/')
    location = host_param[0]
    station = host_param[1] 
    
    json_obj = json.loads(msg.payload)
    db_elems = []

    for key, value in json_obj.items():
        if is_int(value) or is_float(value):
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

    # Add elements in batch.
    db_client.write_points(db_elems)

def broker_connect():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost")
    client.loop_forever()

if __name__ == "__main__":
    broker_connect()