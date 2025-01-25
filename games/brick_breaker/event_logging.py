from datetime import datetime
from supabase import create_client

# Supabase configuration (replace these with your own credentials)
SUPABASE_URL = "https://ujbnbqdnhljivwhnufem.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqYm5icWRuaGxqaXZ3aG51ZmVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MTMzMzAsImV4cCI6MjA1MzM4OTMzMH0.L5dRXYbXivEmOFOe9En-KJB8emRUxHZt5BkzzNhfiG4"

# Create a Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
            "timestamp": timestamp
        }
        response = supabase.table("fsr_events").insert(data).execute()
        print(f"Logged to Supabase: {data}")
    except Exception as e:
        print(f"Error logging to Supabase: {e}")

# Function to handle a batch of FSR data and log the average
def handle_fsr_data(fsr_id, values):
    """
    Calculate the average pressure for a batch of FSR readings and log it.

    Parameters:
        fsr_id (str): Identifier for the FSR (e.g., 'left' or 'right').
        values (list): List of pressure readings.
    """
    if values:
        avg_pressure = sum(values) / len(values)
        log_fsr_event(fsr_id, avg_pressure)
    else:
        print(f"No data to log for {fsr_id}.")
