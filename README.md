# IO uHat for Raspberry Pi Zero 2W

An expansion board (uHat) for the Raspberry Pi Zero 2W that provides additional GPIO and analog input capabilities through I2C and SPI interfaces.

![IO uHat Board](https://hussamtalkstech.com/wp-content/uploads/rpi_io_uhat1-1024x576.jpg)

## Features

- **16 Additional GPIO Pins**: MCP23017 I2C GPIO expander
- **8-Channel 12-bit ADC**: MCP3208 SPI analog-to-digital converter
- **I2C EEPROM**: Compliant with Raspberry Pi uHat specification
- **Hand-Solder Friendly**: SOIC packages for ICs, 1206 packages for passives
- **3.3V Operation**: Compatible with Raspberry Pi GPIO voltage levels

## Hardware Specifications

### GPIO Expander (MCP23017)
- **Interface**: I2C
- **I2C Address**: 0x20
- **GPIO Pins**: 16 general-purpose input/output pins
- **Logic Level**: 3.3V only

### ADC (MCP3208)
- **Interface**: SPI
- **Channels**: 8 single-ended or 4 differential
- **Resolution**: 12-bit
- **Reference Voltage**: 3.3V
- **Input Range**: 0V to 3.3V

### Power Requirements
- **Supply Voltage**: 3.3V from Raspberry Pi
- **Power Source**: Raspberry Pi GPIO header

## Hardware Design

The board features a compact uHat form factor designed for the Raspberry Pi Zero 2W. All components use hand-solder-friendly packages:
- SOIC packages for integrated circuits
- 1206 packages for resistors and capacitors

### Documentation
- [Schematic (PDF)](https://hussamtalkstech.com/wp-content/uploads/GPIO_ADC_uHAT_schematic.pdf)
- KiCad design files available in this repository

## Software

### Python Classes

Two Python classes are provided for easy interfacing:

1. **MCP23017 GPIO Control**: Configure and control the 16 GPIO pins
2. **MCP3208 ADC Interface**: Perform analog-to-digital conversions

### Demo Application

A demonstration program is included that showcases the board's capabilities:
- Reads analog voltage from a potentiometer (connected to ADC)
- Controls a 10-LED bargraph display (connected to GPIO expander)
- LEDs illuminate proportionally to the input voltage (0V = all off, 3.3V = all on)

### Setup

```bash
# Enable I2C and SPI interfaces
sudo raspi-config
# Navigate to Interface Options and enable I2C and SPI

# Verify I2C device detection
i2cdetect -y 1
# Should show device at address 0x20

# Clone repository and run demo
git clone https://github.com/halherta/GPIO_ADC_uHAT
cd GPIO_ADC_uHAT/test_code
python3 demo.py
```

## Getting Started

### Prerequisites
- Raspberry Pi Zero 2W
- Python 3
- I2C and SPI interfaces enabled
- Required Python libraries:
  - `smbus2` (for I2C communication)
  - `spidev` (for SPI communication)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/halherta/GPIO_ADC_uHAT
```

2. Install required Python packages:
```bash
pip3 install smbus2 spidev
```

3. Run the demo program:
```bash
cd test_code
python3 demo.py
```

## Repository Structure

```
.
├── hardware/           # KiCad design files
├── test_code/         # Python classes and demo program
├── docs/              # Additional documentation
└── README.md          # This file
```

## License

This project is open source and available for use under the terms specified in the repository.

## Author

Created by Hussam Halherta - [Hussam Talks Tech](https://hussamtalkstech.com)

## Related Posts

For more detailed information about this project, visit:
- [IO uHat Blog Post](https://hussamtalkstech.com/rpi-io-uhat/)
- Future posts will cover EEPROM configuration and additional applications

## Contributing

Contributions, issues, and feature requests are welcome!

## Acknowledgments

- Designed with KiCad
- Compatible with Raspberry Pi uHat specification
