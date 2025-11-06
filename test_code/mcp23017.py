import smbus
import time

class MCP23017:
    """
    Driver for MCP23017 16-bit I/O Expander with I2C interface.
    
    The MCP23017 provides 16 GPIO pins split into two 8-bit ports (A and B).
    """
    
    # Register addresses
    IODIRA = 0x00    # I/O direction register A
    IODIRB = 0x01    # I/O direction register B
    IPOLA = 0x02     # Input polarity register A
    IPOLB = 0x03     # Input polarity register B
    GPINTENA = 0x04  # Interrupt-on-change enable A
    GPINTENB = 0x05  # Interrupt-on-change enable B
    DEFVALA = 0x06   # Default compare register A
    DEFVALB = 0x07   # Default compare register B
    INTCONA = 0x08   # Interrupt control register A
    INTCONB = 0x09   # Interrupt control register B
    IOCON = 0x0A     # Configuration register
    GPPUA = 0x0C     # Pull-up resistor register A
    GPPUB = 0x0D     # Pull-up resistor register B
    INTFA = 0x0E     # Interrupt flag register A
    INTFB = 0x0F     # Interrupt flag register B
    INTCAPA = 0x10   # Interrupt capture register A
    INTCAPB = 0x11   # Interrupt capture register B
    GPIOA = 0x12     # GPIO register A
    GPIOB = 0x13     # GPIO register B
    OLATA = 0x14     # Output latch register A
    OLATB = 0x15     # Output latch register B
    
    # Port constants
    PORTA = 0
    PORTB = 1
    
    # Direction constants
    INPUT = 1
    OUTPUT = 0
    
    # Logic levels
    HIGH = 1
    LOW = 0
    
    def __init__(self, bus=1, address=0x20):
        """
        Initialize MCP23017 I/O Expander.
        
        Args:
            bus: I2C bus number (default: 1)
            address: I2C address (default: 0x20)
        """
        self.bus = smbus.SMBus(bus)
        self.address = address
        
        # Initialize with all pins as inputs
        self.bus.write_byte_data(self.address, self.IODIRA, 0xFF)
        self.bus.write_byte_data(self.address, self.IODIRB, 0xFF)
        
    def setup_pin(self, pin, direction, port=None, pullup=False):
        """
        Configure a single pin as input or output.
        
        Args:
            pin: Pin number (0-7 for individual port, or 0-15 if port is None)
            direction: INPUT (1) or OUTPUT (0)
            port: PORTA (0) or PORTB (1). If None, pin 0-7 = Port A, 8-15 = Port B
            pullup: Enable internal pull-up resistor (only for inputs)
        """
        if port is None:
            # Legacy mode: pin 0-15
            if not 0 <= pin <= 15:
                raise ValueError("Pin must be 0-15 when port is None")
            port = self.PORTB if pin >= 8 else self.PORTA
            bit = pin % 8
        else:
            # Explicit port mode: pin 0-7
            if not 0 <= pin <= 7:
                raise ValueError("Pin must be 0-7 when port is specified")
            if port not in (self.PORTA, self.PORTB):
                raise ValueError("Port must be PORTA (0) or PORTB (1)")
            bit = pin
        
        # Set direction
        iodir_reg = self.IODIRB if port == self.PORTB else self.IODIRA
        iodir = self.bus.read_byte_data(self.address, iodir_reg)
        
        if direction == self.INPUT:
            iodir |= (1 << bit)  # Set bit to 1 for input
        else:
            iodir &= ~(1 << bit)  # Clear bit to 0 for output
            
        self.bus.write_byte_data(self.address, iodir_reg, iodir)
        
        # Set pull-up if requested
        if pullup and direction == self.INPUT:
            gppu_reg = self.GPPUB if port == self.PORTB else self.GPPUA
            gppu = self.bus.read_byte_data(self.address, gppu_reg)
            gppu |= (1 << bit)
            self.bus.write_byte_data(self.address, gppu_reg, gppu)
    
    def setup_port(self, port, direction_byte):
        """
        Configure entire port (8 pins) at once.
        
        Args:
            port: PORTA (0) or PORTB (1)
            direction_byte: 8-bit value where 1=input, 0=output
        """
        iodir_reg = self.IODIRB if port == self.PORTB else self.IODIRA
        self.bus.write_byte_data(self.address, iodir_reg, direction_byte)
    
    def digital_write(self, pin, value):
        """
        Write digital value to output pin.
        
        Args:
            pin: Pin number (0-15)
            value: HIGH (1) or LOW (0)
        """
        if not 0 <= pin <= 15:
            raise ValueError("Pin must be 0-15")
        
        port = self.PORTB if pin >= 8 else self.PORTA
        bit = pin % 8
        
        # Read current output latch
        olat_reg = self.OLATB if port == self.PORTB else self.OLATA
        olat = self.bus.read_byte_data(self.address, olat_reg)
        
        # Set or clear bit
        if value:
            olat |= (1 << bit)
        else:
            olat &= ~(1 << bit)
        
        self.bus.write_byte_data(self.address, olat_reg, olat)
    
    def digital_read(self, pin):
        """
        Read digital value from input pin.
        
        Args:
            pin: Pin number (0-15)
            
        Returns:
            HIGH (1) or LOW (0)
        """
        if not 0 <= pin <= 15:
            raise ValueError("Pin must be 0-15")
        
        port = self.PORTB if pin >= 8 else self.PORTA
        bit = pin % 8
        
        # Read GPIO register
        gpio_reg = self.GPIOB if port == self.PORTB else self.GPIOA
        gpio = self.bus.read_byte_data(self.address, gpio_reg)
        
        return (gpio >> bit) & 0x01
    
    def write_port(self, port, value):
        """
        Write 8-bit value to entire port.
        
        Args:
            port: PORTA (0) or PORTB (1)
            value: 8-bit value to write
        """
        olat_reg = self.OLATB if port == self.PORTB else self.OLATA
        self.bus.write_byte_data(self.address, olat_reg, value)
    
    def read_port(self, port):
        """
        Read 8-bit value from entire port.
        
        Args:
            port: PORTA (0) or PORTB (1)
            
        Returns:
            8-bit value
        """
        gpio_reg = self.GPIOB if port == self.PORTB else self.GPIOA
        return self.bus.read_byte_data(self.address, gpio_reg)
    
    def set_polarity(self, pin, inverted=False):
        """
        Set input polarity for a pin.
        
        Args:
            pin: Pin number (0-15)
            inverted: If True, GPIO value will be inverted
        """
        if not 0 <= pin <= 15:
            raise ValueError("Pin must be 0-15")
        
        port = self.PORTB if pin >= 8 else self.PORTA
        bit = pin % 8
        
        ipol_reg = self.IPOLB if port == self.PORTB else self.IPOLA
        ipol = self.bus.read_byte_data(self.address, ipol_reg)
        
        if inverted:
            ipol |= (1 << bit)
        else:
            ipol &= ~(1 << bit)
        
        self.bus.write_byte_data(self.address, ipol_reg, ipol)
    
    def close(self):
        """Close I2C connection."""
        self.bus.close()
