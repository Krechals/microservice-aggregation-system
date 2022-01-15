import paho.mqtt.client as mqtt

TOPIC = "sprc/chat/andrei_tudor.topala"
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def broker_publish():
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect("localhost")
    client.loop_start()
    while True:
        msg = input()
        client.publish(TOPIC, msg, qos=2, retain=True)

if __name__ == "__main__":
	broker_publish()