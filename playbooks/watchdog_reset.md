# Playbook: Watchdog Reset Review

## Trigger

ESP32 resets with a watchdog timer (WDT) reset reason in the boot log.

## Symptoms

- Reset reason: `rst:0x7 (TG0WDT_SYS_RESET)` — Task watchdog.
- Reset reason: `rst:0x8 (TG1WDT_SYS_RESET)` — Interrupt watchdog.
- `Task watchdog got triggered` in serial output.
- Periodic resets during specific operations.

## Triage Steps

### Step 1: Identify Watchdog Type

| Reset Code | Type | Timeout | Monitored |
|-----------|------|---------|-----------|
| `TG0WDT_SYS_RESET` | Task WDT | ~5s (default) | IDLE task on each core |
| `TG1WDT_SYS_RESET` | Interrupt WDT | ~300ms | Interrupt handling time |

**Task WDT**: Triggers when the IDLE task on a core cannot run for the configured timeout. This means a task is hogging the CPU without yielding.

**Interrupt WDT**: Triggers when interrupt processing takes too long. This means an ISR is running for too long or interrupts are disabled for too long.

### Step 2: Identify the Blocking Task

The watchdog message shows which task was blocked:

```
E (12345) task_wdt: Task watchdog got triggered. The following tasks did not reset the watchdog in time:
E (12345) task_wdt:  - IDLE0 (CPU 0)
E (12345) task_wdt: Tasks currently running:
E (12345) task_wdt: CPU 0: my_blocking_task
E (12345) task_wdt: CPU 1: IDLE1
```

This tells you `my_blocking_task` is hogging CPU 0.

### Step 3: Find the Blocking Code

Common causes:

**Busy-wait loops:**
```c
// BAD: Blocks forever without yielding
while (!flag_is_set) {
    // No delay, no yield
}

// GOOD: Yield or delay
while (!flag_is_set) {
    vTaskDelay(pdMS_TO_TICKS(10));
}
```

**Long computations without yielding:**
```c
// BAD: Long loop without yield
for (int i = 0; i < 1000000; i++) {
    do_heavy_computation(i);
}

// GOOD: Yield periodically
for (int i = 0; i < 1000000; i++) {
    do_heavy_computation(i);
    if (i % 1000 == 0) {
        vTaskDelay(1);  // Yield to other tasks
    }
}
```

**Disabled interrupts for too long:**
```c
// BAD: Long critical section
taskENTER_CRITICAL(&spinlock);
process_large_buffer(buf, 10000);  // Takes too long
taskEXIT_CRITICAL(&spinlock);

// GOOD: Short critical sections
for (int i = 0; i < 100; i++) {
    taskENTER_CRITICAL(&spinlock);
    process_chunk(buf + i * 100, 100);
    taskEXIT_CRITICAL(&spinlock);
}
```

**Infinite loops in ISR:**
```c
// BAD: Complex logic in ISR
void IRAM_ATTR my_isr(void *arg) {
    while (data_available()) {
        process_data();  // Could take too long
    }
}

// GOOD: Defer work to task
void IRAM_ATTR my_isr(void *arg) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    xTaskNotifyFromISR(worker_task, 0, eNoAction, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

### Step 4: Check Task Priorities

```c
// A high-priority task that never blocks will starve lower priorities
// including the IDLE task (priority 0)
xTaskCreate(my_task, "my_task", 4096, NULL, configMAX_PRIORITIES - 1, NULL);
// If my_task never calls vTaskDelay or blocks on a queue/semaphore,
// the IDLE task never runs → watchdog triggers
```

### Step 5: Feed or Reconfigure the Watchdog

For legitimately long operations:
```c
#include "esp_task_wdt.h"

// Option 1: Feed the watchdog
esp_task_wdt_reset();

// Option 2: Add current task to WDT and manage manually
esp_task_wdt_add(NULL);
// ... long work with periodic esp_task_wdt_reset() ...
esp_task_wdt_delete(NULL);

// Option 3: Increase timeout (in menuconfig)
// CONFIG_ESP_TASK_WDT_TIMEOUT_S=30
```

## Resolution Checklist

- [ ] Watchdog type identified (Task vs Interrupt).
- [ ] Blocking task identified from WDT message.
- [ ] Root cause found (busy-wait, long compute, ISR abuse, priority issue).
- [ ] Fix applied (added yields, deferred ISR work, reduced critical sections).
- [ ] System runs stable under load after fix.

## Prevention

- Never write busy-wait loops without a yield or delay.
- Keep ISRs short — defer complex work to tasks.
- Keep critical sections under 1ms.
- Use appropriate task priorities and always include blocking points.
- Periodically feed the watchdog in legitimately long operations.
