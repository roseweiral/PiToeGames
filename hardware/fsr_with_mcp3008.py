import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 1350000

# Function to read data from MCP3008
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])  # SPI transaction
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Main loop to read FSR values
try:
    while True:
        fsr1_value = read_adc(0)  # Read from CH0
        fsr2_value = read_adc(1)  # Read from CH1
        print(f"FSR1: {fsr1_value}, FSR2: {fsr2_value}")
        time.sleep(0.5)
except KeyboardInterrupt:
    spi.close()
    print("Exiting...")
