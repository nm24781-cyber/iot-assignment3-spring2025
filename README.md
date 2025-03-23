# IoT Assignment 3

This project demonstrates a cloud-based IoT system using MQTT and virtual sensors for temperature, humidity, and CO₂ levels.

## Components

- `script.py`: Publishes random sensor values to `spring2025/iot/envstation` every 10 seconds.
- `scrip1.py`: Subscribes to the topic, stores data in memory, and allows querying:
  - Latest values by station
  - Last 5 hours of values by sensor

## Dependencies

- Python 3.8+
- paho-mqtt

Install dependencies:
```bash
pip install paho-mqtt
