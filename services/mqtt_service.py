import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))

TOPICS = {
    "Emaar Phase 1": os.getenv("MQTT_SITE_A_TOPIC"),
    "Emaar Phase 2": os.getenv("MQTT_SITE_B_TOPIC"),
    "Discovery Dunes": os.getenv("MQTT_SITE_C_TOPIC")
}

latest_data = {
    "Emaar Phase 1": {},
    "Emaar Phase 2": {},
    "Discovery Dunes": {}
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")

        for site, topic in TOPICS.items():
            client.subscribe(topic)
            print(f"Subscribed : {site} -> {topic}")
    else:
        print(f"MQTT connection failed with code : {rc}")

def on_message(client, userdata, msg):

    topic = msg.topic

    payload = msg.payload.decode("utf-8")

    data = json.loads(payload)

    site = None

    for site_name, site_topic in TOPICS.items():

        if site_topic == topic:
            site = site_name
            break

    if site is not None:

        latest_data[site] = data

        print(f"{site} data received")

    else:

        print(f"Unknown MQTT topic: {topic}")


def start_mqtt():

    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)

    client.loop_forever()