# Playbook: I2C Bring-Up

## Trigger

I2C peripheral fails to communicate with a slave device.

## Symptoms

- `i2c_master_cmd_begin()` returns `ESP_ERR_TIMEOUT` or `ESP_FAIL`.
- No ACK from slave device.
- Data corruption or wrong values read.
- Bus hangs (SDA stuck LOW).

## Triage Steps

### Step 1: Verify Pin Selection

```c
#define I2C_SDA_GPIO  21  // Common default
#define I2C_SCL_GPIO  22  // Common default
```

**Check:**
- [ ] SDA and SCL are not on input-only pins (GPIO 34-39).
- [ ] SDA and SCL are not on flash pins (GPIO 6-11).
- [ ] SDA and SCL are not shared with another peripheral.
- [ ] Pins match the physical wiring.

### Step 2: Check Pull-Up Resistors

I2C **requires** pull-up resistors on both SDA and SCL.

| Speed | Recommended Pull-Up |
|-------|-------------------|
| 100 kHz (Standard) | 4.7 kΩ |
| 400 kHz (Fast) | 2.2 kΩ |
| 1 MHz (Fast+) | 1 kΩ |

**Critical:** ESP32 internal pull-ups (~45 kΩ) are **too weak** for reliable I2C. Always use external pull-ups.

```c
// DO NOT rely on this for I2C:
i2c_config.scl_pullup_en = GPIO_PULLUP_ENABLE;  // Weak, unreliable
i2c_config.sda_pullup_en = GPIO_PULLUP_ENABLE;  // Weak, unreliable

// ALWAYS use external resistors
```

### Step 3: Verify I2C Configuration

```c
i2c_config_t conf = {
    .mode = I2C_MODE_MASTER,
    .sda_io_num = I2C_SDA_GPIO,
    .scl_io_num = I2C_SCL_GPIO,
    .sda_pullup_en = GPIO_PULLUP_DISABLE,  // Use external
    .scl_pullup_en = GPIO_PULLUP_DISABLE,  // Use external
    .master.clk_speed = 100000,  // Start slow for debugging
};
```

**Common mistakes:**
- Using wrong I2C port number (ESP32 has I2C_NUM_0 and I2C_NUM_1).
- Clock speed too high for the bus capacitance.
- Forgetting `i2c_param_config()` before `i2c_driver_install()`.

### Step 4: Verify Slave Address

- I2C addresses are 7-bit. Some datasheets show 8-bit (with R/W bit).
- If datasheet says `0xD0`, the 7-bit address is `0x68`.
- Check if the address is different for your variant or if address pins (A0, A1, A2) are set.

**Scan the bus:**
```c
for (uint8_t addr = 1; addr < 127; addr++) {
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(I2C_NUM_0, cmd, pdMS_TO_TICKS(50));
    i2c_cmd_link_delete(cmd);
    if (ret == ESP_OK) {
        ESP_LOGI(TAG, "Found device at 0x%02X", addr);
    }
}
```

### Step 5: Check Timeout Values

```c
// Default timeout may be too short for slow devices
i2c_set_timeout(I2C_NUM_0, 0xFFFFF);  // Maximum timeout
```

### Step 6: Bus Recovery

If SDA is stuck LOW (bus hang):
```c
// Manual bus recovery — toggle SCL to release SDA
gpio_set_direction(I2C_SCL_GPIO, GPIO_MODE_OUTPUT);
for (int i = 0; i < 9; i++) {
    gpio_set_level(I2C_SCL_GPIO, 1);
    vTaskDelay(pdMS_TO_TICKS(1));
    gpio_set_level(I2C_SCL_GPIO, 0);
    vTaskDelay(pdMS_TO_TICKS(1));
}
// Re-initialize I2C driver after recovery
```

## Resolution Checklist

- [ ] Pin selection verified (not reserved, not shared).
- [ ] External pull-up resistors present and correct value.
- [ ] Slave address confirmed (7-bit format).
- [ ] I2C bus scan finds the device.
- [ ] Communication succeeds at 100 kHz.
- [ ] Speed increased after confirming basic communication.

## Prevention

- Always start bring-up at 100 kHz before increasing speed.
- Always use external pull-ups.
- Document pin assignments in a pin map.
- Implement bus recovery in production code.
- Add timeout handling for all I2C operations.
