from datetime import datetime
from supabase import create_client
import time


# Supabase URL and Key (replace these with your own credentials)
SUPABASE_URL = "https://ujbnbqdnhljivwhnufem.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqYm5icWRuaGxqaXZ3aG51ZmVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MTMzMzAsImV4cCI6MjA1MzM4OTMzMH0.L5dRXYbXivEmOFOe9En-KJB8emRUxHZt5BkzzNhfiG4"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Threshold to detect pressure events
THRESHOLD = 100

# Function to log to Supabase
def log_fsr_event(fsr_id, fsr_value):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "fsr_id": fsr_id,
            "average_pressure": fsr_value,
            "timestamp": timestamp
        }
        response = supabase.table("fsr_events").insert(data).execute()
        print(f"Logged to Supabase: {data}")
    except Exception as e:
        print(f"Error logging to Supabase: {e}")

# Function to calculate averages and log to Supabase
def handle_fsr_data(fsr_id, values):
    if values:
        avg_pressure = sum(values) / len(values)
        log_fsr_event(fsr_id, avg_pressure)
    else:
        print(f"No data to log for {fsr_id}.")

# Simulation of FSR readings
def send_sample_data():
    left_values = []
    right_values = []
    is_left_above = False
    is_right_above = False

    for i in range(500):  # Simulate 50 entries
        fsr_value_left = 90 + (i % 50)  # Simulated oscillating values for left
        fsr_value_right = 70 + (i % 50)  # Simulated oscillating values for right
        print(fsr_value_left, fsr_value_right)

        # Handle left FSR
        if fsr_value_left > THRESHOLD:
            left_values.append(fsr_value_left)
            is_left_above = True
        elif is_left_above:  # Value dropped below threshold
            handle_fsr_data("left", left_values)
            left_values = []
            is_left_above = False

        # Handle right FSR
        if fsr_value_right > THRESHOLD:
            right_values.append(fsr_value_right)
            is_right_above = True
        elif is_right_above:  # Value dropped below threshold
            handle_fsr_data("right", right_values)
            right_values = []
            is_right_above = False

        #time.sleep(0.1)  # Small delay between readings

    # Final check to send any remaining data
    print("Finalizing remaining data...")
    if left_values:
        handle_fsr_data("left", left_values)
    if right_values:
        handle_fsr_data("right", right_values)

# Run the simulation
if __name__ == "__main__":
    send_sample_data()
