# Playbook: Wi-Fi Failure Investigation

## Trigger

ESP32 fails to connect to Wi-Fi, drops connection frequently, or never reaches IP assignment.

## Symptoms

- `WIFI_EVENT_STA_DISCONNECTED` events in logs.
- No `IP_EVENT_STA_GOT_IP` event.
- Connection timeout.
- Intermittent drops during operation.

## Triage Steps

### Step 1: Check Initialization Sequence

The correct order is:
1. `nvs_flash_init()` — Wi-Fi stores calibration data in NVS.
2. `esp_netif_init()` — Initialize network interface.
3. `esp_event_loop_create_default()` — Create system event loop.
4. `esp_netif_create_default_wifi_sta()` — Create STA interface.
5. `esp_wifi_init()` with `WIFI_INIT_CONFIG_DEFAULT()`.
6. Register event handlers.
7. `esp_wifi_set_mode(WIFI_MODE_STA)`.
8. `esp_wifi_set_config()` with credentials.
9. `esp_wifi_start()`.

**Common mistakes:**
- Forgetting `nvs_flash_init()` → Wi-Fi fails silently or with opaque errors.
- Registering event handlers after `esp_wifi_start()` → Missing early events.
- Not calling `esp_netif_create_default_wifi_sta()` → No IP assignment.

### Step 2: Check Credentials

```c
wifi_config_t wifi_config = {
    .sta = {
        .ssid = "YourSSID",          // Max 32 chars
        .password = "YourPassword",   // Max 64 chars, min 8 for WPA2
    },
};
```

**Common mistakes:**
- SSID or password has trailing whitespace or null characters.
- SSID is case-sensitive.
- Password shorter than 8 characters for WPA2.
- Using WPA3 without `CONFIG_ESP_WIFI_ENABLE_WPA3_SAE=y`.

### Step 3: Check Disconnect Reason

The `WIFI_EVENT_STA_DISCONNECTED` event provides a reason code:

| Reason Code | Meaning | Likely Cause |
|------------|---------|-------------|
| 2 | AUTH_EXPIRE | Authentication timed out |
| 15 | 4WAY_HANDSHAKE_TIMEOUT | Wrong password |
| 201 | NO_AP_FOUND | SSID not in range or wrong SSID |
| 202 | AUTH_FAIL | Authentication rejected |
| 203 | ASSOC_FAIL | Association failed |
| 7 | NOT_ASSOCED | Not associated before sending data |
| 8 | DISASSOC_STA_LEAVING | AP kicked the station |

```c
// In event handler:
wifi_event_sta_disconnected_t *event = (wifi_event_sta_disconnected_t *)event_data;
ESP_LOGW(TAG, "Disconnected, reason: %d", event->reason);
```

### Step 4: Check Event Handler

```c
static void wifi_event_handler(void *arg, esp_event_base_t event_base,
                                int32_t event_id, void *event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        // Reconnect logic here
        esp_wifi_connect();
    }
}

static void ip_event_handler(void *arg, esp_event_base_t event_base,
                              int32_t event_id, void *event_data)
{
    if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t *event = (ip_event_got_ip_t *)event_data;
        ESP_LOGI(TAG, "Got IP: " IPSTR, IP2STR(&event->ip_info.ip));
    }
}
```

### Step 5: Check Reconnection Logic

- Is reconnection attempted after disconnect?
- Is there a backoff to avoid rapid-fire reconnects?
- Is the retry count limited or infinite?
- Is the Wi-Fi driver restarted after too many failures?

### Step 6: Check RF Environment

- Is the AP within range?
- Is the antenna connected (for external antenna boards)?
- Is there RF interference?
- Is the AP's DHCP server working?
- Is MAC filtering enabled on the AP?

## Resolution Checklist

- [ ] Init sequence verified.
- [ ] Credentials verified.
- [ ] Disconnect reason code captured and interpreted.
- [ ] Event handlers registered correctly.
- [ ] Reconnection logic with backoff implemented.
- [ ] Tested with known-good AP.

## Prevention

- Always log disconnect reason codes.
- Implement robust reconnection with backoff.
- Use Kconfig for credentials, not hardcoded strings.
- Test with AP power cycle to validate reconnect.
- Monitor RSSI for marginal signal strength.
