# MQTT Telemetry Node Template

> Wi-Fi + MQTT client with automatic reconnection, JSON payload publishing, last will and testament, and configurable topics.

## Features

- Wi-Fi station with exponential backoff reconnection.
- MQTT client with auto-reconnect.
- JSON telemetry publishing (sensor data, heap, uptime).
- Last Will and Testament (LWT) for online/offline status.
- Configurable via menuconfig (Wi-Fi, MQTT broker, topics).
- Clean event-driven architecture.

## Usage

```bash
cp -r templates/mqtt-node/ ~/my-mqtt-project/
cd ~/my-mqtt-project/
idf.py set-target esp32
idf.py menuconfig  # Set Wi-Fi and MQTT broker
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

## MQTT Topics

| Topic | Direction | Content |
|-------|-----------|---------|
| `device/{id}/telemetry` | Publish | JSON sensor data |
| `device/{id}/status` | Publish (LWT) | `online` / `offline` |
