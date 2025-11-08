# MCP23017 & MCP3208 Python Drivers

Python drivers for interfacing with the MCP23017 I2C GPIO expander and MCP3208 SPI ADC converter on Raspberry Pi and similar platforms.

## Overview

This package provides two driver classes:

- **MCP23017**: 16-bit I/O expander with I2C interface (16 GPIO pins split into two 8-bit ports)
- **MCP3208**: 12-bit 8-channel analog-to-digital converter with SPI interface

## Requirements

```bash
pip install spidev smbus
```

## MCP23017 - I2C GPIO Expander

### Features

- 16 GPIO pins organized as Port A (pins 0-7) and Port B (pins 8-15)
- Configurable as inputs or outputs
- Internal pull-up resistors for inputs
- Input polarity inversion
- Port-wide or individual pin control

### Basic Usage

```python
from mcp23017 import MCP23017

# Initialize (default: I2C bus 1, address 0x20)
gpio = MCP23017(bus=1, address=0x20)

# Configure pin 0 as output
gpio.setup_pin(0, gpio.OUTPUT)

# Configure pin 8 as input with pull-up
gpio.setup_pin(8, gpio.INPUT, pullup=True)

# Write to output pin
gpio.digital_write(0, gpio.HIGH)
gpio.digital_write(0, gpio.LOW)

# Read from input pin
value = gpio.digital_read(8)
print(f"Pin 8 state: {value}")

# Clean up
gpio.close()
```

### Port-Based Operations

```python
# Configure entire Port A as outputs (0x00 = all outputs)
gpio.setup_port(gpio.PORTA, 0x00)

# Write 8-bit value to Port A (binary: 10101010)
gpio.write_port(gpio.PORTA, 0xAA)

# Read entire Port B
port_value = gpio.read_port(gpio.PORTB)
print(f"Port B value: 0x{port_value:02X}")
```

### LED Blink Example

```python
from mcp23017 import MCP23017
import time

gpio = MCP23017()

# Setup pin 0 as output
gpio.setup_pin(0, gpio.OUTPUT)

# Blink LED 10 times
for i in range(10):
    gpio.digital_write(0, gpio.HIGH)
    time.sleep(0.5)
    gpio.digital_write(0, gpio.LOW)
    time.sleep(0.5)

gpio.close()
```

### Button Input Example

```python
from mcp23017 import MCP23017
import time

gpio = MCP23017()

# Setup pin 8 as input with pull-up resistor
gpio.setup_pin(8, gpio.INPUT, pullup=True)

print("Monitoring button on pin 8 (Press Ctrl+C to exit)")
try:
    while True:
        button_state = gpio.digital_read(8)
        if button_state == gpio.LOW:  # Button pressed (active low)
            print("Button pressed!")
            time.sleep(0.2)  # Debounce delay
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    gpio.close()
```

## MCP3208 - SPI ADC Converter

### Features

- 12-bit resolution (0-4095)
- 8 single-ended or 4 differential input channels
- Configurable reference voltage
- SPI interface with adjustable clock speed

### Basic Usage

```python
from mcp3208 import MCP3208

# Initialize (default: SPI bus 0, device 0, 1MHz)
adc = MCP3208(bus=0, device=0, max_speed_hz=1000000)

# Read raw 12-bit value from channel 0
raw_value = adc.read_channel(0)
print(f"Raw value: {raw_value}")

# Read voltage from channel 0 (assuming 3.3V reference)
voltage = adc.read_voltage(0, vref=3.3)
print(f"Voltage: {voltage:.3f}V")

# Clean up
adc.close()
```

### Reading Multiple Channels

```python
from mcp3208 import MCP3208
import time

adc = MCP3208()

print("Reading from all 8 channels:")
for channel in range(8):
    voltage = adc.read_voltage(channel, vref=3.3)
    print(f"Channel {channel}: {voltage:.3f}V")

adc.close()
```

### Differential Mode

```python
from mcp3208 import MCP3208

adc = MCP3208()

# Read differential voltage between channel pairs
# Channel 0: reads (CH0 - CH1)
# Channel 1: reads (CH2 - CH3)
# Channel 2: reads (CH4 - CH5)
# Channel 3: reads (CH6 - CH7)

diff_value = adc.read_channel(0, mode='diff')
diff_voltage = adc.read_voltage(0, vref=3.3, mode='diff')
print(f"Differential (CH0-CH1): {diff_voltage:.3f}V")

adc.close()
```

### Temperature Sensor Example (with TMP36)

```python
from mcp3208 import MCP3208
import time

adc = MCP3208()

print("Reading temperature from TMP36 on channel 0")
print("Press Ctrl+C to exit\n")

try:
    while True:
        # Read voltage from TMP36 sensor
        voltage = adc.read_voltage(0, vref=3.3)
        
        # Convert to temperature (TMP36: 10mV/°C, 500mV offset)
        temperature_c = (voltage - 0.5) * 100
        temperature_f = (temperature_c * 9/5) + 32
        
        print(f"Voltage: {voltage:.3f}V | Temp: {temperature_c:.1f}°C / {temperature_f:.1f}°F")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    adc.close()
```

### Potentiometer Reading Example

```python
from mcp3208 import MCP3208
import time

adc = MCP3208()

print("Reading potentiometer on channel 0")
print("Press Ctrl+C to exit\n")

try:
    while True:
        raw = adc.read_channel(0)
        voltage = adc.read_voltage(0, vref=3.3)
        percentage = (raw / 4095.0) * 100
        
        print(f"Raw: {raw:4d} | Voltage: {voltage:.3f}V | Position: {percentage:.1f}%")
        time.sleep(0.5)
        
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    adc.close()
```

## Pin Numbering

### MCP23017
- Pins 0-7: Port A
- Pins 8-15: Port B
- Can use either global pin numbering (0-15) or port-specific (0-7 with port parameter)

### MCP3208
- Channels 0-7: Single-ended mode
- Channels 0-3: Differential mode

## I2C Addresses (MCP23017)

The MCP23017 default address is 0x20, but can be configured using the A0, A1, A2 pins:

- A2 A1 A0 → Address
- 0  0  0  → 0x20 (default)
- 0  0  1  → 0x21
- 0  1  0  → 0x22
- ...
- 1  1  1  → 0x27

## Wiring

### MCP23017 (I2C)
```
MCP23017    Raspberry Pi
VDD     →   3.3V
VSS     →   GND
SCL     →   SCL (GPIO 3)
SDA     →   SDA (GPIO 2)
RESET   →   3.3V
```

### MCP3208 (SPI)
```
MCP3208     Raspberry Pi
VDD     →   3.3V
VREF    →   3.3V
AGND    →   GND
DGND    →   GND
CLK     →   SCLK (GPIO 11)
DOUT    →   MISO (GPIO 9)
DIN     →   MOSI (GPIO 10)
CS/SHDN →   CE0 (GPIO 8)
```

## License

These drivers are provided as-is for educational and development purposes.

## Notes

- Enable I2C and SPI interfaces using `raspi-config` on Raspberry Pi
- The MCP3208 reference voltage (VREF) determines the maximum measurable voltage
- For accurate ADC readings, use a stable voltage reference
- Pull-up resistors on MCP23017 are approximately 10kΩ
