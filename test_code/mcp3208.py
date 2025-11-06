import spidev
import smbus
import time


class MCP3208:
    """
    Driver for MCP3208 12-bit ADC with 8 channels using SPI interface.
    
    The MCP3208 is a 12-bit analog-to-digital converter with 8 single-ended
    or 4 differential input channels.
    """
    
    def __init__(self, bus=0, device=0, max_speed_hz=1000000):
        """
        Initialize MCP3208 ADC.
        
        Args:
            bus: SPI bus number (default: 0)
            device: SPI device number (default: 0)
            max_speed_hz: SPI clock speed in Hz (default: 1MHz)
        """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = 0  # SPI mode 0,0
        
    def read_channel(self, channel, mode='single'):
        """
        Read analog value from specified channel.
        
        Args:
            channel: Channel number (0-7 for single-ended, 0-3 for differential)
            mode: 'single' for single-ended or 'diff' for differential
            
        Returns:
            12-bit integer value (0-4095)
        """
        if mode == 'single':
            if not 0 <= channel <= 7:
                raise ValueError("Single-ended channel must be 0-7")
            # Start bit, single-ended mode (1), channel selection
            cmd = 0x06 | ((channel & 0x04) >> 2)
            data = [(channel & 0x03) << 6, 0]
        elif mode == 'diff':
            if not 0 <= channel <= 3:
                raise ValueError("Differential channel must be 0-3")
            # Start bit, differential mode (0), channel selection
            cmd = 0x04 | ((channel & 0x04) >> 2)
            data = [(channel & 0x03) << 6, 0]
        else:
            raise ValueError("Mode must be 'single' or 'diff'")
        
        # Send command and receive data
        response = self.spi.xfer2([cmd] + data)
        
        # Extract 12-bit value from response
        value = ((response[1] & 0x0F) << 8) | response[2]
        return value
    
    def read_voltage(self, channel, vref=3.3, mode='single'):
        """
        Read voltage from specified channel.
        
        Args:
            channel: Channel number
            vref: Reference voltage (default: 3.3V)
            mode: 'single' or 'diff'
            
        Returns:
            Voltage as float
        """
        value = self.read_channel(channel, mode)
        voltage = (value * vref) / 4096.0
        return voltage
    
    def close(self):
        """Close SPI connection."""
        self.spi.close()
