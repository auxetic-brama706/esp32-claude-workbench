# Mission: ESP32 Wi-Fi Reconnect Handler

## Goal

Implement a robust Wi-Fi reconnection handler that automatically reconnects after disconnection with exponential backoff, connection status tracking, and configurable retry limits.

## Board / Target

- **Chip**: ESP32
- **Board**: ESP32-DevKitC
- **ESP-IDF version**: v5.2

## Constraints

- Must not block other FreeRTOS tasks during reconnection.
- Maximum retry interval: 60 seconds.
- Must log all state transitions.
- Must expose connection status via a public API.
- Memory budget: < 1 KB additional heap usage.

## Files in Scope

| File | Action | Notes |
|------|--------|-------|
| `main/wifi_manager.h` | CREATE | Public API for Wi-Fi management |
| `main/wifi_manager.c` | CREATE | Implementation with event-driven reconnect |
| `main/main.c` | MODIFY | Integrate Wi-Fi manager into app startup |
| `main/Kconfig.projbuild` | CREATE | Configurable SSID, password, retry limits |

## Design Notes

- Use ESP-IDF event loop (`esp_event`) for Wi-Fi state changes.
- Reconnection runs in a dedicated FreeRTOS task with 4096 byte stack.
- Backoff sequence: 1s → 2s → 4s → 8s → 16s → 32s → 60s (capped).
- Connection status stored in an atomic variable for thread-safe reads.
- Event group used to signal connection/disconnection to waiting tasks.

### Rejected Alternatives
- Timer-based reconnect: Rejected because it complicates cleanup and does not support backoff easily.
- Polling-based: Rejected for unnecessary CPU usage.

## Acceptance Criteria

- [ ] Wi-Fi connects on boot with configured credentials.
- [ ] Automatic reconnection after AP disconnect with exponential backoff.
- [ ] Retry count and backoff reset after successful reconnection.
- [ ] Connection status queryable via `wifi_manager_is_connected()`.
- [ ] All state transitions logged at `ESP_LOGI` level.
- [ ] No blocking calls in the reconnection logic.
- [ ] Configurable via menuconfig (SSID, password, max retries).
- [ ] Compiles cleanly with no warnings.

## Test Plan

- [ ] **Host test**: Backoff calculation logic (1, 2, 4, 8, 16, 32, 60, 60...).
- [ ] **Host test**: Retry counter reset after max retries.
- [ ] **Build test**: Project compiles with default sdkconfig.
- [ ] **Target test**: Connects to Wi-Fi AP on boot (requires hardware).
- [ ] **Target test**: Reconnects after AP power cycle (requires hardware).

## Known Risks

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Wi-Fi credentials hardcoded | LOW | Using Kconfig, not hardcoded strings |
| Stack overflow in reconnect task | LOW | 4096 bytes is generous for this task |
| Event loop memory | LOW | Using default system event loop |

## Current Status

- **State**: NOT STARTED
- **Last updated**: 2026-03-26
- **Completed items**: Mission created
- **Blocking issues**: None

## Next Step

Create implementation contract and get it approved.

## History

| Date | Action | Notes |
|------|--------|-------|
| 2026-03-26 | Created | Initial mission from Wi-Fi reconnect requirement |
