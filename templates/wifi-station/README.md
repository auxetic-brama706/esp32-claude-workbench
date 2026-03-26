# Wi-Fi Station Template

> Production-ready Wi-Fi station with automatic reconnection, exponential backoff, NVS credential storage, and event-driven architecture.

## Features

- Event-driven Wi-Fi management (no polling).
- Automatic reconnection with exponential backoff (1s → 60s).
- Connection status API for other tasks.
- Configurable via menuconfig (SSID, password, max retries).
- Clean shutdown and resource cleanup.
- Proper error handling on all paths.

## Usage

```bash
cp -r templates/wifi-station/ ~/my-wifi-project/
cd ~/my-wifi-project/
idf.py set-target esp32
idf.py menuconfig  # Set Wi-Fi SSID and password
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```
