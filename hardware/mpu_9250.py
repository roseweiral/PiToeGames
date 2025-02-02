import time
import board
import busio
import adafruit_icm20x

# Initialize I2C connection
i2c = busio.I2C(board.SCL, board.SDA)

# Create ICM-20948 objects for both sensors with different I2C addresses
sensor1 = adafruit_icm20x.ICM20948(i2c, address=0x68)  # Address for Sensor 1
sensor2 = adafruit_icm20x.ICM20948(i2c, address=0x69)  # Address for Sensor 2

while True:
    # Read data from Sensor 1
    accel_x1, accel_y1, accel_z1 = sensor1.acceleration
    gyro_x1, gyro_y1, gyro_z1 = sensor1.gyro
    mag_x1, mag_y1, mag_z1 = sensor1.magnetic

    # Read data from Sensor 2
    accel_x2, accel_y2, accel_z2 = sensor2.acceleration
    gyro_x2, gyro_y2, gyro_z2 = sensor2.gyro
    mag_x2, mag_y2, mag_z2 = sensor2.magnetic

    # Print data from both sensors
    print(f"Gyro X={gyro_x1:.2f}, Y={gyro_y1:.2f}, Z={gyro_z1:.2f},X={gyro_x2:.2f}, Y={gyro_y2:.2f}, Z={gyro_z2:.2f}")
    #print(f"Sensor 1 - Accel (m/s^2): X={accel_x1:.2f}, Y={accel_y1:.2f}, Z={accel_z1:.2f}")
    #print(f"Sensor 1 - Mag (uT): X={mag_x1:.2f}, Y={mag_y1:.2f}, Z={mag_z1:.2f}")
    #print("========================")
    #print("")
    #print("========================")
    
    #print(f"Sensor 2 - Gyro (deg/s): X={gyro_x2:.2f}, Y={gyro_y2:.2f}, Z={gyro_z2:.2f}")
    #print(f"Sensor 2 - Accel (m/s^2): X={accel_x2:.2f}, Y={accel_y2:.2f}, Z={accel_z2:.2f}")
    #print(f"Sensor 2 - Mag (uT): X={mag_x2:.2f}, Y={mag_y2:.2f}, Z={mag_z2:.2f}")
    time.sleep(0.1)
