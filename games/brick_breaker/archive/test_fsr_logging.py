import random
from event_logging import handle_fsr_data

def process_fsr_stream(stream):
    """
    Process a mixed stream of FSR readings for both left and right sensors.

    Parameters:
        stream (list): List of tuples (fsr_id, reading), where fsr_id is
                       'left' or 'right' and reading is the pressure value.
    """
    for fsr_id, reading in stream:
        print(f"Sending {fsr_id}: {reading}")
        handle_fsr_data(fsr_id, [reading])  # Send each reading as a single-item list
        print("===================================")

    # Send a final value of 0 for both "left" and "right"
    for fsr_id in ["left", "right"]:
        print(f"Sending {fsr_id}: 0 (final flush)")
        handle_fsr_data(fsr_id, [0])
        print("===================================")

if __name__ == "__main__":
    # Generate a mixed stream of 1000 FSR readings
    stream = []
    for _ in range(1000):
        fsr_id = random.choice(["left", "right"])  # Randomly select sensor ID
        reading = random.randint(90, 200)  # Generate random pressure value
        stream.append((fsr_id, reading))

    print("Processing mixed FSR stream...")
    process_fsr_stream(stream)
    print("Processing complete.")
