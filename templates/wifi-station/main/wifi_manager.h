/**
 * @file wifi_manager.h
 * @brief Wi-Fi station manager with automatic reconnection and exponential backoff.
 */

#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include "esp_err.h"
#include <stdbool.h>

/**
 * @brief Initialize and start the Wi-Fi station manager.
 *
 * Sets up the Wi-Fi driver, event handlers, and starts connection.
 * Connection runs asynchronously — use wifi_manager_wait_connected()
 * to block until connected.
 *
 * @return ESP_OK on success.
 */
esp_err_t wifi_manager_init(void);

/**
 * @brief Check if Wi-Fi is currently connected.
 *
 * Thread-safe. Can be called from any task.
 *
 * @return true if connected and IP assigned.
 */
bool wifi_manager_is_connected(void);

/**
 * @brief Block until Wi-Fi is connected or timeout expires.
 *
 * @param timeout_ms Maximum time to wait in milliseconds. 0 = wait forever.
 * @return ESP_OK if connected, ESP_ERR_TIMEOUT if timed out.
 */
esp_err_t wifi_manager_wait_connected(uint32_t timeout_ms);

/**
 * @brief Shut down the Wi-Fi manager and release resources.
 */
void wifi_manager_shutdown(void);

#endif /* WIFI_MANAGER_H */
