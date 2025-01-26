from datetime import datetime
from supabase import create_client
import time

# Supabase URL and Key (replace these with your own credentials)
SUPABASE_URL = "https://ujbnbqdnhljivwhnufem.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqYm5icWRuaGxqaXZ3aG51ZmVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MTMzMzAsImV4cCI6MjA1MzM4OTMzMH0.L5dRXYbXivEmOFOe9En-KJB8emRUxHZt5BkzzNhfiG4"

# Create a Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Threshold to detect when the FSR is pressed and released
THRESHOLD = 100

# Function to log a single FSR event to Supabase
def log_fsr_event(fsr_id, avg_pressure):
    try:
        # Convert Unix timestamp to SQL-compatible format
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")

        data = {
            "fsr_id": fsr_id,
            "average_pressure": avg_pressure,
            "timestamp": timestamp  # Use formatted timestamp
        }
        # Insert into Supabase
        response = supabase.table("fsr_events").insert(data).execute()
        print(f"Logged to Supabase: {data}")
    except Exception as e:
        print(f"Error logging to Supabase: {e}")

# Function to calculate average pressure while FSR is pressed
def process_fsr_data(fsr_id, fsr_values):
    if len(fsr_values) > 0:
        avg_pressure = sum(fsr_values) / len(fsr_values)  # Calculate the average
        log_fsr_event(fsr_id, avg_pressure)  # Log to Supabase
        print(f"{fsr_id} FSR avg: {avg_pressure:.2f}")  # Log to console
    else:
        print(f"No values to average for {fsr_id}")

# Simulated FSR data with averaging logic
def send_sample_data():
    left_fsr_values = []  # To hold values while above threshold
    right_fsr_values = []
    
    for i in range(500):  # Simulate 50 entries
        fsr_value_left = 80 + (i % 50)  # Simulated oscillating values for left
        fsr_value_right = 70 + (i % 50)  # Simulated oscillating values for right

        # Process left FSR
        if fsr_value_left > THRESHOLD:
            left_fsr_values.append(fsr_value_left)
        elif left_fsr_values:
            process_fsr_data("left", left_fsr_values)
            left_fsr_values = []  # Reset after logging

        # Process right FSR
        if fsr_value_right > THRESHOLD:
            right_fsr_values.append(fsr_value_right)
        elif right_fsr_values:
            process_fsr_data("right", right_fsr_values)
            right_fsr_values = []  # Reset after logging

        print(f"Left: {fsr_value_left}, Right: {fsr_value_right}")  # Log raw values
        time.sleep(0.1)  # Small delay between entries

# Run the simulation
if __name__ == "__main__":
    send_sample_data()
