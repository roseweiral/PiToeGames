from datetime import datetime
from supabase import create_client
import json

# ANSI escape code for red font color
RED = "\033[31m"
RESET = "\033[0m"


# Supabase configuration (replace these with your own credentials)
SUPABASE_URL = "https://ujbnbqdnhljivwhnufem.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqYm5icWRuaGxqaXZ3aG51ZmVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MTMzMzAsImV4cCI6MjA1MzM4OTMzMH0.L5dRXYbXivEmOFOe9En-KJB8emRUxHZt5BkzzNhfiG4"

# Create a Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Threshold for logging
THRESHOLD = 100

# State storage for accumulating readings
accumulator = {
    "left": {"values": [], "above_threshold": False},
    "right": {"values": [], "above_threshold": False},
}

# Function to log an FSR event to Supabase
def log_fsr_event(fsr_id, fsr_value):
    """
    Log a single FSR event to Supabase.

    Parameters:
        fsr_id (str): Identifier for the FSR (e.g., 'left' or 'right').
        fsr_value (float): Average pressure value to log.
    """
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "fsr_id": fsr_id,
            "average_pressure": fsr_value,
            "timestamp": timestamp,
        }
        print(f"Logging to Supabase: {json.dumps(data, indent=2)}")
        response = supabase.table("fsr_events").insert(data).execute()
        print(f"Logged to Supabase: {data}")
    except Exception as e:
        print(f"Error logging to Supabase: {e}")



# Function to handle an individual FSR reading
def handle_fsr_data(fsr_id, values):
    
    if not values:
        return

    fsr_state = accumulator[fsr_id]

    if values > THRESHOLD:
        fsr_state["values"].append(values)
        fsr_state["above_threshold"] = True
    else:
        if fsr_state["above_threshold"]:
            # Log the average of accumulated values
            avg_pressure = sum(fsr_state["values"]) / len(fsr_state["values"])
            log_fsr_event(fsr_id, avg_pressure)

            # Reset the accumulator for this sensor
            fsr_state["values"] = []
            fsr_state["above_threshold"] = False

