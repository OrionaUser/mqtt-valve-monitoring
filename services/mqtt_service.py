import os
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))

TOPICS = {
    "Emaar South Phase 1": os.getenv("MQTT_SITE_A_TOPIC"),
    "Emaar South Phase 2": os.getenv("MQTT_SITE_B_TOPIC"),
    "Discovery Dunes": os.getenv("MQTT_SITE_C_TOPIC")
}

COMMAND_TOPICS = {
    "Emaar South Phase 1": "EBO/TEST/101",
    "Emaar South Phase 2": "EBO/TEST/202",
    "Discovery Dunes": "EBO/TEST/303"
}

latest_data = {
    "Emaar South Phase 1": {},
    "Emaar South Phase 2": {},
    "Discovery Dunes": {}
}

client = None

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


def publish_valve_command(site: str, command: str):

    if command not in ["1","2"]:
        raise ValueError("Invalid valve command")

    if client is None:
        raise RuntimeError("MQTT client is not initialized")

    if site not in COMMAND_TOPICS:
        raise ValueError(f"Unknown site : {site}")
    
    payload = {
        "Threshold": None,
        "valve_cmd": command
    }

    command_topic = COMMAND_TOPICS[site]

    result = client.publish(
        command_topic,
        json.dumps(payload)
    )

    return result

def start_mqtt():
    global client
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)

    client.loop_forever()

