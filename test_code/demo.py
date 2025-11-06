from mcp23017 import MCP23017
from mcp3208 import MCP3208
import time

DIGITS = {
        0: 0b00111111,  # 0
        1: 0b00000110,  # 1
        2: 0b01011011,  # 2
        3: 0b01001111,  # 3
        4: 0b01100110,  # 4
        5: 0b01101101,  # 5
        6: 0b01111101,  # 6
        7: 0b00000111,  # 7
        8: 0b01111111,  # 8
        9: 0b01101111,  # 9
    }

io = MCP23017(bus=1, address=0x20)
adc = MCP3208(bus=0, device=0)

# Configure portb as output
io.setup_port(io.PORTB, 0x00)


# Blink LED on pin 0
for i in range(100):
    value = adc.read_channel(0)
    voltage = adc.read_voltage(0)
    
    print(f"Channel 0: {value} ({voltage:.3f}V)")
    
    if value >= 0 and value <= 409: 
        io.write_port(io.PORTB, 0b00000000)
    elif value > 409 and value <= 2*409: 
        io.write_port(io.PORTB, 0b00000001)
    elif value > 2*409 and value <= 3*409: 
        io.write_port(io.PORTB, 0b00000011)
    elif value > 3*409 and value <= 4*409: 
        io.write_port(io.PORTB, 0b00000111)
    elif value > 4*409 and value <= 5*409: 
        io.write_port(io.PORTB, 0b00001111)
    elif value > 5*409 and value <= 6*409: 
        io.write_port(io.PORTB, 0b00011111)
    elif value > 6*409 and value <= 7*409: 
        io.write_port(io.PORTB, 0b00111111)
    elif value > 7*409 and value <= 8*409: 
        io.write_port(io.PORTB, 0b01111111)
    else: 
        io.write_port(io.PORTB, 0b11111111)
    time.sleep(0.5)

io.close()
adc.close()
