from datetime import datetime
from supabase import create_client
import time


# Supabase URL and Key (replace these with your own credentials)
SUPABASE_URL = "https://ujbnbqdnhljivwhnufem.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqYm5icWRuaGxqaXZ3aG51ZmVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MTMzMzAsImV4cCI6MjA1MzM4OTMzMH0.L5dRXYbXivEmOFOe9En-KJB8emRUxHZt5BkzzNhfiG4"

# Create a Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to log a single FSR event to Supabase
def log_fsr_event(fsr_id, fsr_value):
    try:
        # Convert Unix timestamp to SQL-compatible format
        timestamp = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        
        data = {
            "fsr_id": fsr_id,
            "average_pressure": fsr_value,
            "timestamp": timestamp  # Use formatted timestamp
        }
        # Insert into Supabase
        response = supabase.table("fsr_events").insert(data).execute()
        print(f"Logged to Supabase: {data}")
    except Exception as e:
        print(f"Error logging to Supabase: {e}")

# Simulated FSR data
def send_sample_data():
    for i in range(10):  # Send 10 entries
        fsr_value_left = 600 + i  # Simulated increasing values for left
        fsr_value_right = 700 - i  # Simulated decreasing values for right

        log_fsr_event("left", fsr_value_left)
        log_fsr_event("right", fsr_value_right)

        time.sleep(0.5)  # Small delay between entries

# Run the simulation
if __name__ == "__main__":
    send_sample_data()