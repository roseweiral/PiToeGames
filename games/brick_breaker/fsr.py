# fsr.py
import random

# FSR Constants
FSR_CHANNEL_LEFT = 0  # FSR connected to CH0 for left movement
FSR_CHANNEL_RIGHT = 1  # FSR connected to CH1 for right movement
FSR_THRESHOLD = 100  # Sensitivity threshold for FSRs

fsr_simulation_mode = False

# Try to import spidev for the Raspberry Pi; simulate FSR input otherwise
try:
    import spidev
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1350000

    def read_adc(channel):
        """Read data from the specified ADC channel."""
        if channel < 0 or channel > 7:
            return -1
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
except (ImportError, FileNotFoundError):
    print("spidev not found. Running in simulation mode.")
    fsr_simulation_mode = True

    def read_adc(channel):
        """Simulate ADC readings for testing on non-Raspberry Pi systems."""
        return random.randint(0, 200)  # Simulated ADC value


def get_fsr_values():
    """Read and return FSR values for both left and right channels."""
    fsr_value_left = read_adc(FSR_CHANNEL_LEFT)
    fsr_value_right = read_adc(FSR_CHANNEL_RIGHT)
    return fsr_value_left, fsr_value_right
