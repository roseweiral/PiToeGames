import random
import time
import threading

# FSR Constants
FSR_CHANNEL_LEFT = 0  # FSR connected to CH0 for left movement
FSR_CHANNEL_RIGHT = 1  # FSR connected to CH1 for right movement
FSR_THRESHOLD = 100  # Sensitivity threshold for FSRs

fsr_simulation_mode = False
print(f"FSR simulation mode: {fsr_simulation_mode}")
FSR_SIMULATION_RATE = 1.0  # Delay in seconds between simulated readings

# Shared variable for storing FSR readings
fsr_values = {
    'left': 0,
    'right': 0
}

# Try to import spidev for the Raspberry Pi; simulate FSR input otherwise
try:
    from Adafruit_ADS1x15 import ADS1115

    # Initialize ADS1115 ADC
    adc = ADS1115(busnum=1)
    GAIN = 1  # You can adjust the gain if needed

    def read_adc(channel):
        """Read data from the specified ADC channel."""
        # Reads from the ADC and returns the value
        return adc.read_adc(channel, gain=GAIN)
    
except (ImportError, FileNotFoundError):
    print("ADS115 not found Running Simulation.")
    fsr_simulation_mode = True
    print(f"FSR simulation mode: {fsr_simulation_mode}")

    def read_adc(channel):
        """Simulate ADC readings for testing on non-Raspberry Pi systems."""
        return random.randint(0, 10)  # Simulated ADC value

def simulate_fsr():
    """Simulate FSR values in a separate thread."""
    while True:
        fsr_values['left'] = read_adc(FSR_CHANNEL_LEFT)
        fsr_values['right'] = read_adc(FSR_CHANNEL_RIGHT)
        print(f"Simulated FSR values: {fsr_values}")
        time.sleep(FSR_SIMULATION_RATE)  # Delay in simulation (non-blocking)

# Start the simulation in a separate thread
if fsr_simulation_mode:
    fsr_thread = threading.Thread(target=simulate_fsr)
    fsr_thread.daemon = True  # Daemonize the thread to exit when the main program exits
    fsr_thread.start()

def get_fsr_values():
    """Get the latest FSR values."""
    print(f"FSR values: {fsr_values}")
    return fsr_values['left'], fsr_values['right']
