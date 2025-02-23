import time
import threading
from Adafruit_ADS1x15 import ADS1115

# FSR Constants
FSR_CHANNEL_LEFT = 0  # FSR connected to CH0 for left movement
FSR_CHANNEL_RIGHT = 1  # FSR connected to CH1 for right movement
FSR_THRESHOLD = 100  # Sensitivity threshold for FSRs

# Initialize ADS1115 ADC
adc = ADS1115()
GAIN = 1  # You can adjust the gain if needed

# Shared variable for storing FSR readings
fsr_values = {
    'left': 0,
    'right': 0
}

def read_adc(channel):
    """Read data from the specified ADC channel."""
    # Reads from the ADC and returns the value
    return adc.read_adc(channel, gain=GAIN)

def simulate_fsr():
    """Simulate FSR values in a separate thread (for demonstration or testing)."""
    while True:
        # Read actual FSR values from the ADC
        fsr_values['left'] = read_adc(FSR_CHANNEL_LEFT)
        fsr_values['right'] = read_adc(FSR_CHANNEL_RIGHT)
        
        # Output the values for debugging or game logic
        print(f"FSR values: Left={fsr_values['left']}, Right={fsr_values['right']}")
        
        # Sleep for a short time to avoid flooding the console
        time.sleep(0.1)

# Start the simulation in a separate thread
fsr_thread = threading.Thread(target=simulate_fsr)
fsr_thread.daemon = True  # Daemonize the thread to exit when the main program exits
fsr_thread.start()

def get_fsr_values():
    """Get the latest FSR values."""
    # Retrieve and return the latest values
    return fsr_values['left'], fsr_values['right']

def is_left_pressed():
    """Check if left FSR has crossed the threshold."""
    return fsr_values['left'] > FSR_THRESHOLD

def is_right_pressed():
    """Check if right FSR has crossed the threshold."""
    return fsr_values['right'] > FSR_THRESHOLD

# Example usage in the game loop (simulation or real usage)
while True:
    # Get the current values from the FSRs
    left, right = get_fsr_values()

    # Check if either left or right FSR has been pressed
    if is_left_pressed():
        print("Left FSR pressed!")
    
    if is_right_pressed():
        print("Right FSR pressed!")
    
    # Implement the logic for game control based on FSR values here
    # (e.g., move a character or trigger an event)
    
    time.sleep(0.1)  # Adjust the loop delay for game logic
