from datetime import datetime
from pytz import timezone
import paho.mqtt.client as mqtt
import json
import random

def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}.')

def broker_publish():
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect("localhost")
    client.loop_start()
    tz = timezone('Europe/Bucharest')

    topics = ["UPB/Mongo", "UPB/Gas", "UPB/Cherry", "Andrei/Fox", "UPB/Phoenix", "Andrei/Doom", "Andrei/Zeus"]
    
    msg = {
        'BAT': round(random.uniform(70.01, 99.99), 2),
        'HUMID': round(random.uniform(30.01, 39.99), 2),
        'TMP': round(random.uniform(19.99, 29.99), 2),
        'PRJ': 'SPRC',
        'status': 'OK',
    }
    if round(random.uniform(0, 1)) == 0:
        msg['timestamp'] = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z')

    client.publish(topics[round(random.uniform(0, len(topics) - 1))], json.dumps(msg), qos=2, retain=True)
    print(f'Successfully published.')
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
	broker_publish()