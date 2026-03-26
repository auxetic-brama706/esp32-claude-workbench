# Playbook: BLE Debugging

## Trigger

BLE fails to initialize, advertise, connect, or maintain stable communication.

## Symptoms

- BLE stack fails to start.
- Advertising starts but no device is visible to scanners.
- Connection drops immediately after establishment.
- GATT read/write operations return errors.
- MTU negotiation fails or data is truncated.
- Pairing/bonding fails.
- Coexistence issues with Wi-Fi.

## Triage Steps

### Step 1: Verify BLE Initialization Sequence

The correct NimBLE initialization order:
```c
// 1. Initialize NVS (required for BLE bonding storage)
nvs_flash_init();

// 2. Initialize NimBLE host stack
esp_nimble_hci_init();
nimble_port_init();

// 3. Configure and register GATT services
ble_svc_gap_init();
ble_svc_gatt_init();
// ... register your custom services ...

// 4. Set device name
ble_svc_gap_device_name_set("MyDevice");

// 5. Configure and start the host task
ble_hs_cfg.sync_cb = ble_on_sync;
ble_hs_cfg.reset_cb = ble_on_reset;
nimble_port_freertos_init(ble_host_task);
```

For Bluedroid (legacy):
```c
esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
esp_bt_controller_init(&bt_cfg);
esp_bt_controller_enable(ESP_BT_MODE_BLE);
esp_bluedroid_init();
esp_bluedroid_enable();
esp_ble_gap_register_callback(gap_event_handler);
esp_ble_gatts_register_callback(gatts_event_handler);
```

**Common mistakes:**
- Forgetting `nvs_flash_init()` → bonding data lost.
- Wrong BT mode → using `ESP_BT_MODE_CLASSIC_BT` instead of `ESP_BT_MODE_BLE`.
- Not releasing classic BT memory when only using BLE:
  ```c
  ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));
  ```

### Step 2: Check sdkconfig BLE Settings

```
# Essential BLE settings
CONFIG_BT_ENABLED=y
CONFIG_BT_NIMBLE_ENABLED=y          # Use NimBLE (recommended)
CONFIG_BT_NIMBLE_MAX_CONNECTIONS=3   # Adjust as needed

# Memory optimization for BLE-only
CONFIG_BT_CONTROLLER_ONLY=n
CONFIG_BT_BLUEDROID_ENABLED=n        # If using NimBLE
```

**If using Wi-Fi + BLE simultaneously:**
```
CONFIG_SW_COEXIST_ENABLE=y           # CRITICAL - enables Wi-Fi/BLE coexistence
CONFIG_ESP_COEX_SW_COEXIST_ENABLE=y  # ESP-IDF 5.x name
```

### Step 3: Debug Connection Problems

**Device not visible during scanning:**
- Verify advertising is started in the `sync_cb` callback.
- Check advertising parameters (interval, type).
- Verify device name length (max 29 bytes in adv data for BLE 4.2).
- Check if advertising uses correct address type.

**Connection drops immediately:**
- Check connection interval parameters (min/max).
- Verify supervision timeout (must be > connection interval × max events).
- Check if the peripheral sends an immediate disconnect.

```c
// Reasonable connection parameters:
struct ble_gap_conn_params conn_params = {
    .itvl_min = 24,    // 30ms (24 * 1.25ms)
    .itvl_max = 40,    // 50ms
    .latency = 0,
    .supervision_timeout = 256,  // 2.56s
};
```

### Step 4: Debug GATT Issues

**Service not discovered by client:**
- Ensure services are registered BEFORE advertising starts.
- Check UUID format (16-bit vs 128-bit).
- Verify attribute table is not too large for available memory.

**Read/Write operations fail:**
- Check that callback functions handle the correct operation types.
- Verify attribute permissions match the operation (e.g., write requires `BLE_GATT_CHR_F_WRITE`).
- Check that response data fits within the current MTU.

### Step 5: Debug MTU Negotiation

Default BLE MTU is 23 bytes (20 bytes payload). For larger transfers:

```c
// Request larger MTU after connection
ble_att_set_preferred_mtu(512);  // NimBLE
// or
esp_ble_gatt_set_local_mtu(512);  // Bluedroid
```

**Common MTU issues:**
- Sending data larger than negotiated MTU → data truncated silently.
- Not waiting for MTU exchange complete event before sending large data.
- Peer device doesn't support requested MTU → falls back to 23.

### Step 6: Debug Pairing/Bonding

```c
// NimBLE security configuration
ble_hs_cfg.sm_io_cap = BLE_SM_IO_CAP_NO_IO;  // Just Works pairing
ble_hs_cfg.sm_bonding = 1;
ble_hs_cfg.sm_mitm = 0;
ble_hs_cfg.sm_sc = 1;  // Secure Connections
```

**Bonding failures:**
- NVS full → can't store bond info. Erase and re-bond.
- Too many bonded devices → increase `CONFIG_BT_NIMBLE_MAX_BONDS`.
- iOS/Android cached old bond → delete bond on phone, re-pair.
- `sm_mitm = 1` but `sm_io_cap = BLE_SM_IO_CAP_NO_IO` → incompatible.

## Resolution Checklist

- [ ] BLE initialization sequence is correct.
- [ ] sdkconfig has correct BLE settings.
- [ ] Wi-Fi/BLE coexistence enabled (if both used).
- [ ] Classic BT memory released (if only using BLE).
- [ ] Advertising parameters are valid.
- [ ] GATT services registered before advertising.
- [ ] MTU negotiated before large transfers.
- [ ] Bonding storage has space in NVS.

## Prevention

- Use NimBLE over Bluedroid for lower memory usage and simpler API.
- Release classic BT memory to save ~60 KB heap.
- Always enable Wi-Fi/BLE coexistence if using both.
- Test with multiple BLE clients (iOS, Android, nRF Connect).
- Monitor heap usage — BLE stack needs significant memory.
- Implement disconnect/reconnect handling in the application.
