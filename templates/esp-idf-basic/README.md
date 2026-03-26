# ESP-IDF Basic Template

> Minimal ESP-IDF project ready for Claude Workbench workflow.

## Usage

```bash
# Copy template to new project
cp -r templates/esp-idf-basic/ ~/my-new-project/
cd ~/my-new-project/

# Set target
idf.py set-target esp32

# Build
idf.py build

# Flash and monitor
idf.py -p /dev/ttyUSB0 flash monitor
```

## Structure

```
esp-idf-basic/
├── CMakeLists.txt           # Root build file
├── main/
│   ├── CMakeLists.txt       # Main component build file
│   └── main.c               # Application entry point
├── sdkconfig.defaults       # Default configuration
└── README.md                # This file
```

## Customization

1. Rename the project in root `CMakeLists.txt`.
2. Add components as subdirectories with their own `CMakeLists.txt`.
3. Extend `sdkconfig.defaults` with your configuration.
4. Create a mission file in the workbench for your task.
