"""
subscriber script
1. Subscribes to spring2025/iot/envstation
2. Stores data in memory
3. Provides 2 functions:
    3.1 Show latest sensor data from a specific station
    3.2 Show all data from last 5 hours for a specific sensor
"""

import json
import time
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt

# Configuration
BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "spring2025/iot/envstation"

# In-memory storage
sensor_data_log = []  # List of all messages
latest_station_data = {}  # Dict to track latest values per station_id


def on_connect(client, userdata, flags, rc):
    print("✅ Connected to broker")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        timestamp = datetime.strptime(payload["timestamp"], "%Y-%m-%d %H:%M:%S")
        payload["timestamp"] = timestamp

        # Add to log
        sensor_data_log.append(payload)

        # Update latest data for this station
        station_id = payload["station_id"]
        latest_station_data[station_id] = payload

        print(f"📥 Received from {station_id}: {payload}")

    except Exception as e:
        print(f"⚠️ Failed to process message: {e}")


# Utility: Show latest sensor data for a station
def show_latest_from_station(station_id):
    print(f"\n📊 Latest data for station '{station_id}':")
    data = latest_station_data.get(station_id)
    if data:
        print(json.dumps(data, indent=2, default=str))
    else:
        print("No data found for this station.")


# Utility: Show last 5 hours of data for a sensor type
def show_last_5_hours(sensor_type):
    print(f"\n📊 Sensor history for '{sensor_type}' (last 5 hours):")
    now = datetime.now()
    cutoff = now - timedelta(hours=5)
    count = 0

    for entry in sensor_data_log:
        if entry["timestamp"] >= cutoff:
            print(f"{entry['timestamp']}: {entry['station_id']} → {sensor_type} = {entry.get(sensor_type)}")
            count += 1

    if count == 0:
        print("No recent data found.")


# Set up client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()


if __name__ == '__main__':
    # Main loop
    try:
        while True:
            print("\n--- MENU ---")
            print("1. Show latest sensor data from a station")
            print("2. Show last 5 hours of data for a sensor type")
            print("3. Exit")
            choice = input("Enter choice: ")

            if choice == "1":
                station = input("Enter station ID: ")
                show_latest_from_station(station)
            elif choice == "2":
                sensor = input("Enter sensor name (temperature/humidity/co2): ")
                show_last_5_hours(sensor)
            elif choice == "3":
                break
            else:
                print("Invalid option.")

    except KeyboardInterrupt:
        print("⛔ Exiting...")
    finally:
        client.loop_stop()
        client.disconnect()