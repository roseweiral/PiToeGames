import sys
import os

print(sys.path)
print("Current working directory:", os.getcwd())

hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hardware'))
print("Hardware path:", hardware_path)
sys.path.append(hardware_path)

# List contents of the hardware directory
print("Contents of hardware directory:", os.listdir(hardware_path))

# Try importing the fsr module
try:
    from hardware import fsr
    print("FSR module imported successfully.")
except ModuleNotFoundError as e:
    print(f"Error importing fsr: {e}")


import sys
import os

print(sys.path)
print("Current working directory:", os.getcwd())

hardware_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../hardware'))
print("Hardware path:", hardware_path)
sys.path.append(hardware_path)

# List contents of the hardware directory
print("Contents of hardware directory:", os.listdir(hardware_path))

# Try importing the fsr module
try:
    import fsr
    print("FSR module imported successfully.")
except ModuleNotFoundError as e:
    print(f"Error importing fsr: {e}")