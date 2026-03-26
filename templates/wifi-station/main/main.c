/**
 * @file main.c
 * @brief Wi-Fi Station Template — Application Entry Point
 */

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "wifi_manager.h"

static const char *TAG = "main";

void app_main(void)
{
    ESP_LOGI(TAG, "=== Wi-Fi Station Template ===");

    /* Start Wi-Fi */
    ESP_ERROR_CHECK(wifi_manager_init());

    /* Wait for connection (30 second timeout) */
    ESP_LOGI(TAG, "Waiting for Wi-Fi connection...");
    esp_err_t ret = wifi_manager_wait_connected(30000);
    if (ret == ESP_OK) {
        ESP_LOGI(TAG, "Wi-Fi connected!");
    } else {
        ESP_LOGW(TAG, "Wi-Fi not connected yet, continuing anyway...");
    }

    /* Application main loop */
    while (1) {
        if (wifi_manager_is_connected()) {
            ESP_LOGI(TAG, "Status: Connected | Heap: %lu bytes",
                     esp_get_free_heap_size());
        } else {
            ESP_LOGW(TAG, "Status: Disconnected (reconnecting...) | Heap: %lu bytes",
                     esp_get_free_heap_size());
        }
        vTaskDelay(pdMS_TO_TICKS(10000));
    }
}
