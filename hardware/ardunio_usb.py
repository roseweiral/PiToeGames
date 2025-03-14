import serial
import time

# Open serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        ser.write(b"Received: " + line.encode('utf-8') + b"\n")
