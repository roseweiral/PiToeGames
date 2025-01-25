import time
import statistics
from supabase import create_client, Client

# Initialize Supabase client
url = "https://ujbnbqdnhljivwhnufem.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVqYm5icWRuaGxqaXZ3aG51ZmVtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MTMzMzAsImV4cCI6MjA1MzM4OTMzMH0.L5dRXYbXivEmOFOe9En-KJB8emRUxHZt5BkzzNhfiG4"
supabase: Client = create_client(url, key)

try:
    response = supabase.table("fsr_events").select("*").limit(1).execute()
    print("Supabase test query succeeded:", response.data)
except Exception as e:
    print("Error connecting to Supabase:", e)


# FSR event data structure
class FSRData:
    def __init__(self, fsr_id):
        self.fsr_id = fsr_id
        self.accumulated_values = []  # Store all values above threshold
        self.threshold = 100  # Set threshold value for press detection
        self.pressed = False
        self.press_start_time = None

    def update(self, fsr_value):
        """
        Update the FSR data based on the current FSR value.
        If the value is above the threshold, accumulate it.
        """
        current_time = time.time()

        if fsr_value > self.threshold and not self.pressed:
            # Start accumulating values when above threshold
            self.pressed = True
            self.accumulated_values = [fsr_value]  # Start accumulating values
        elif fsr_value > self.threshold and self.pressed:
            # Continue accumulating values while above threshold
            self.accumulated_values.append(fsr_value)
        elif fsr_value < self.threshold and self.pressed:
            # Once below the threshold, calculate the average of the accumulated values
            if len(self.accumulated_values) > 0:
                avg_value = sum(self.accumulated_values) / len(self.accumulated_values)
                self.accumulated_values = []  # Reset for the next press
                self.pressed = False
                return avg_value
        return None  # No value to return if not under the threshold

    def reset(self):
        self.accumulated_values = []

# Function to send data to Supabase
def log_fsr_to_supabase(fsr_data: FSRData):
    avg_value = fsr_data.update(fsr_value=600)  # Pass an example value to simulate
    if avg_value is not None:
        data = {
            "fsr_id": fsr_data.fsr_id,
            "average_pressure": avg_value,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        # Send to Supabase
        response = supabase.table("fsr_events").insert(data).execute()
        print(f"Logged FSR {fsr_data.fsr_id} with avg value: {avg_value} to Supabase.")
        return response
    return None

# Example usage
if __name__ == "__main__":
    # Example FSR data tracking for FSR Left and Right
    fsr_left = FSRData(fsr_id="left")
    fsr_right = FSRData(fsr_id="right")
    
    for _ in range(10):  # Simulate 10 events with varying values
        value_left = 600 if _ % 2 == 0 else 40  # Alternate between above and below threshold
        value_right = 700 if _ % 2 == 0 else 30
            
        avg_left = fsr_left.update(value_left)
        avg_right = fsr_right.update(value_right)

        print(f"Left FSR avg: {avg_left}, Right FSR avg: {avg_right}")  # Debug output
        
        if avg_left is not None:
            print("Logging left FSR to Supabase...")
            log_fsr_to_supabase(fsr_left)
        
        if avg_right is not None:
            print("Logging right FSR to Supabase...")
            log_fsr_to_supabase(fsr_right)

    
    # Reset data for next session
    fsr_left.reset()
    fsr_right.reset()