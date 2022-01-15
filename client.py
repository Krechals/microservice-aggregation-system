import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pytz import timezone

TOPIC = "UPB/RPi_1"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def broker_publish():
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect("localhost")
    client.loop_start()
    tz = timezone('Europe/Bucharest')

    msg = {
        'BAT': 99,
        'HUMID': 40,
        'TMP': 25.3,
        'PRJ': 'SPRC',
        'status': 'OK',
        'timestamp': datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S%z')
    }
    client.publish(TOPIC, json.dumps(msg), qos=2, retain=True)

    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
	broker_publish()