/**
 * @file main.c
 * @brief MQTT Telemetry Node — Wi-Fi + MQTT with JSON publishing.
 *
 * Connects to Wi-Fi, establishes MQTT, and publishes periodic telemetry.
 * Includes Last Will and Testament for online/offline tracking.
 */

#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_netif.h"
#include "nvs_flash.h"
#include "mqtt_client.h"

static const char *TAG = "mqtt_node";

/* State */
static esp_mqtt_client_handle_t s_mqtt_client = NULL;
static volatile bool s_wifi_connected = false;
static volatile bool s_mqtt_connected = false;

/* ---- Wi-Fi ---- */

static void wifi_event_handler(void *arg, esp_event_base_t event_base,
                                int32_t event_id, void *event_data)
{
    static int s_retry = 0;
    static int s_backoff_ms = 1000;

    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        s_wifi_connected = false;
        ESP_LOGW(TAG, "Wi-Fi disconnected, retry in %d ms...", s_backoff_ms);
        vTaskDelay(pdMS_TO_TICKS(s_backoff_ms));
        s_backoff_ms = (s_backoff_ms * 2 > 60000) ? 60000 : s_backoff_ms * 2;
        s_retry++;
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t *event = (ip_event_got_ip_t *)event_data;
        ESP_LOGI(TAG, "Wi-Fi connected, IP: " IPSTR, IP2STR(&event->ip_info.ip));
        s_wifi_connected = true;
        s_retry = 0;
        s_backoff_ms = 1000;
    }
}

static void wifi_init(void)
{
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL, NULL));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_event_handler, NULL, NULL));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = CONFIG_WIFI_SSID,
            .password = CONFIG_WIFI_PASSWORD,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
}

/* ---- MQTT ---- */

static void mqtt_event_handler(void *arg, esp_event_base_t event_base,
                                int32_t event_id, void *event_data)
{
    esp_mqtt_event_handle_t event = (esp_mqtt_event_handle_t)event_data;

    switch (event->event_id) {
    case MQTT_EVENT_CONNECTED:
        ESP_LOGI(TAG, "MQTT connected");
        s_mqtt_connected = true;
        /* Publish online status */
        esp_mqtt_client_publish(s_mqtt_client,
            CONFIG_MQTT_STATUS_TOPIC, "online", 0, 1, 1);
        break;

    case MQTT_EVENT_DISCONNECTED:
        ESP_LOGW(TAG, "MQTT disconnected");
        s_mqtt_connected = false;
        break;

    case MQTT_EVENT_ERROR:
        ESP_LOGE(TAG, "MQTT error type: %d", event->error_handle->error_type);
        break;

    default:
        break;
    }
}

static void mqtt_init(void)
{
    esp_mqtt_client_config_t mqtt_cfg = {
        .broker.address.uri = CONFIG_MQTT_BROKER_URI,
        .session.last_will = {
            .topic = CONFIG_MQTT_STATUS_TOPIC,
            .msg = "offline",
            .msg_len = 7,
            .qos = 1,
            .retain = 1,
        },
    };

    s_mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(s_mqtt_client, ESP_EVENT_ANY_ID,
                                    mqtt_event_handler, NULL);
    esp_mqtt_client_start(s_mqtt_client);
}

/* ---- Telemetry ---- */

static void telemetry_task(void *pvParameters)
{
    char payload[256];
    uint32_t uptime_s = 0;

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(CONFIG_TELEMETRY_INTERVAL_MS));
        uptime_s += CONFIG_TELEMETRY_INTERVAL_MS / 1000;

        if (!s_mqtt_connected) {
            continue;
        }

        /* Build JSON payload */
        snprintf(payload, sizeof(payload),
            "{\"uptime_s\":%lu,\"free_heap\":%lu,\"min_heap\":%lu,\"wifi_rssi\":%d}",
            (unsigned long)uptime_s,
            (unsigned long)esp_get_free_heap_size(),
            (unsigned long)esp_get_minimum_free_heap_size(),
            0  /* Replace with actual RSSI reading */
        );

        int msg_id = esp_mqtt_client_publish(
            s_mqtt_client, CONFIG_MQTT_TELEMETRY_TOPIC, payload, 0, 0, 0);

        ESP_LOGI(TAG, "Published telemetry (msg_id=%d): %s", msg_id, payload);
    }
}

/* ---- Main ---- */

void app_main(void)
{
    ESP_LOGI(TAG, "=== MQTT Telemetry Node ===");

    /* Initialize NVS */
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    /* Start Wi-Fi */
    wifi_init();

    /* Wait for Wi-Fi before starting MQTT */
    ESP_LOGI(TAG, "Waiting for Wi-Fi...");
    while (!s_wifi_connected) {
        vTaskDelay(pdMS_TO_TICKS(100));
    }

    /* Start MQTT */
    mqtt_init();

    /* Start telemetry publishing task */
    xTaskCreate(telemetry_task, "telemetry", 4096, NULL, 5, NULL);

    ESP_LOGI(TAG, "MQTT node running. Publishing every %d ms.",
             CONFIG_TELEMETRY_INTERVAL_MS);
}
