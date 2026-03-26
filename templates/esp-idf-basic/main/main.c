/**
 * @file main.c
 * @brief ESP-IDF Basic Template — Application Entry Point
 *
 * Minimal starting point for an ESP-IDF project. Initializes NVS,
 * logs system information, and enters the main loop.
 */

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"

static const char *TAG = "main";

/**
 * @brief Initialize Non-Volatile Storage (NVS).
 *
 * Required by many ESP-IDF components including Wi-Fi.
 * Handles first-boot initialization and flash corruption recovery.
 */
static void init_nvs(void)
{
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_LOGW(TAG, "NVS partition truncated, erasing...");
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    ESP_LOGI(TAG, "NVS initialized");
}

/**
 * @brief Application entry point.
 */
void app_main(void)
{
    ESP_LOGI(TAG, "=== ESP-IDF Basic Template ===");
    ESP_LOGI(TAG, "IDF version: %s", esp_get_idf_version());
    ESP_LOGI(TAG, "Free heap: %lu bytes", esp_get_free_heap_size());

    init_nvs();

    /* Application initialization goes here */
    ESP_LOGI(TAG, "Application started successfully");

    /* Main loop — replace with your application logic */
    while (1) {
        ESP_LOGI(TAG, "Heap: %lu bytes free", esp_get_free_heap_size());
        vTaskDelay(pdMS_TO_TICKS(10000));
    }
}
