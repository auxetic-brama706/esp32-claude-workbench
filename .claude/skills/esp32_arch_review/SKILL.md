---
name: esp32_arch_review
description: Review ESP32 firmware architecture for RTOS safety, memory management, error handling, and embedded best practices.
---

# ESP32 Architecture Review

Perform a structured review of firmware architecture focusing on embedded-specific safety and correctness.

## When to Use

- Before merging significant changes.
- During implementation contract review.
- When inheriting or auditing an existing project.
- Periodically for long-running projects.

## Review Checklist

### 1. FreeRTOS Safety

- [ ] All tasks have explicitly sized stacks (no defaults).
- [ ] Stack sizes are appropriate: ≥2048 for simple, ≥4096 for Wi-Fi/BLE tasks.
- [ ] No blocking calls in ISRs.
- [ ] ISR-safe API variants used where required (`*FromISR` functions).
- [ ] Shared resources protected by mutexes.
- [ ] No priority inversion risks (or priority inheritance mutexes used).
- [ ] Task watchdog timer handled for long-running operations.
- [ ] No unbounded loops without `vTaskDelay()` or `taskYIELD()`.
- [ ] Critical sections are short (< 1ms).
- [ ] Queue/semaphore usage has appropriate timeouts (not `portMAX_DELAY` everywhere).

### 2. Memory Management

- [ ] No large stack-allocated buffers (> 512 bytes).
- [ ] Heap allocations checked for NULL.
- [ ] DMA buffers allocated with `heap_caps_malloc(MALLOC_CAP_DMA)`.
- [ ] Free heap monitored at runtime.
- [ ] No memory leaks in error paths (allocated memory freed on failure).
- [ ] String buffers have bounds checking.
- [ ] No `malloc()` inside ISRs.

### 3. Error Handling

- [ ] All `esp_err_t` return values checked.
- [ ] `ESP_ERROR_CHECK()` used only for fatal init errors.
- [ ] Runtime errors handled gracefully (log + recover or degrade).
- [ ] Network operations use retry with backoff.
- [ ] Timeout values are defined and reasonable.
- [ ] Error paths clean up resources (close handles, free memory).

### 4. Peripheral Safety

- [ ] GPIO pins validated against reserved pin list.
- [ ] Peripheral initialization checks for errors.
- [ ] De-initialization / cleanup paths exist.
- [ ] Bus recovery mechanisms for I2C/SPI.
- [ ] ADC2 not used alongside Wi-Fi.
- [ ] Pin map is documented and consistent with code.

### 5. Networking

- [ ] Wi-Fi event handler registered properly.
- [ ] Reconnection logic with backoff.
- [ ] TLS certificates validated (not disabled).
- [ ] Hostname/IP validation.
- [ ] Socket timeouts configured.
- [ ] DNS resolution errors handled.

### 6. Persistent Storage

- [ ] NVS keys are namespaced.
- [ ] NVS read errors handled (first-boot defaults).
- [ ] Partition table matches `sdkconfig`.
- [ ] OTA partition scheme is correct.
- [ ] SPIFFS/LittleFS properly initialized and error-checked.

### 7. Logging Quality

- [ ] Appropriate log levels used (E/W/I/D/V).
- [ ] No sensitive data in logs (passwords, tokens).
- [ ] Log tags match component names.
- [ ] Verbose logs behind `ESP_LOGD`/`ESP_LOGV` (not `ESP_LOGI`).
- [ ] Boot sequence is traceable through logs.

### 8. Build Configuration

- [ ] Target chip matches actual hardware.
- [ ] `sdkconfig.defaults` captures all non-default settings.
- [ ] Component dependencies declared in `CMakeLists.txt`.
- [ ] No unused components included.
- [ ] Partition table appropriate for the use case.

## Output

Generate a review report:

```markdown
# Architecture Review Report

## Summary
[Overall assessment: PASS / PASS WITH NOTES / FAIL]

## Critical Issues
- [Issues that must be fixed]

## Warnings
- [Issues that should be addressed]

## Recommendations
- [Improvements to consider]

## Checklist Results
[Filled checklist from above]
```
