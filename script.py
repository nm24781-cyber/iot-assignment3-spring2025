import random
import time
import json
import paho.mqtt.client as mqtt

# Configuration
BROKER = "test.mosquitto.org"  # Or use your HiveMQ Cloud broker
PORT = 1883
TOPIC = "spring2025/iot/envstation"
STATION_ID = "station_A1"  # Unique ID for this virtual station
PUBLISH_INTERVAL = 10  # seconds

def generate_sensor_data():
    return {
        "station_id": STATION_ID,
        "temperature": round(random.uniform(-50, 50), 2),
        "humidity": round(random.uniform(0, 100), 2),
        "co2": round(random.uniform(300, 2000), 2),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
    else:
        print(f"❌ Connection failed with code {rc}")

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        while True:
            data = generate_sensor_data()
            payload = json.dumps(data)
            client.publish(TOPIC, payload)
            print(f"📡 Published: {payload}")
            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("⛔ Stopped by user.")
        client.loop_stop()
        client.disconnect()
