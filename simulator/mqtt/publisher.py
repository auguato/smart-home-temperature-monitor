"""
publisher.py
Publishes simulated sensor readings to HiveMQ cloud broker via MQTT.
Topic: home/temperature
"""

import json
import time
import paho.mqtt.client as mqtt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'simulator'))
from sensor_sim import get_simulated_reading


BROKER   = "broker.hivemq.com"   
PORT     = 1883
TOPIC    = "home/temperature"
INTERVAL = 10                  


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to HiveMQ broker at {BROKER}")
    else:
        print(f"Connection failed with code {rc}")


def on_publish(client, userdata, mid):
    print(f"  Message {mid} published successfully.")


def run():
    client = mqtt.Client(client_id="smart-home-sim-01")
    client.on_connect = on_connect
    client.on_publish  = on_publish

    print(f"Connecting to {BROKER}:{PORT} ...")
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            reading = get_simulated_reading()
            payload = json.dumps(reading)
            result  = client.publish(TOPIC, payload, qos=1)
            print(f"[{reading['timestamp']}] Published → {payload}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nStopping publisher.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run()
