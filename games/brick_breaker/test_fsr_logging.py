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
        handle_fsr_data(fsr_id, [reading])  # Send each reading as a single-item list
        print(f"{fsr_id}: {reading}")


if __name__ == "__main__":
    # Generate a mixed stream of 1000 FSR readings
    stream = []
    for _ in range(10):
        fsr_id = random.choice(["left", "right"])  # Randomly select sensor ID
        reading = random.randint(190, 900)  # Generate random pressure value
        stream.append((fsr_id, reading))

    print("Processing mixed FSR stream...")
    process_fsr_stream(stream)
    print("Processing complete.")
