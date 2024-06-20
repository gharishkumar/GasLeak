#sudo pip3 install gpiozero adafruit-circuitpython-ads1x15
#sudo nano /boot/firmware/config.txt enable_uart=1
from gpiozero import Servo

import board
import time
import serial
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize GPS
SERIAL_PORT = "/dev/serial0"
gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
 
# Create an ADS1115 object
ads = ADS.ADS1115(i2c)
 
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)
 
servo = Servo(6)
servo.min()

def formatDegreesMinutes(coordinates, digits):
    parts = coordinates.split(".")
    if (len(parts) != 2):
        return coordinates
    if (digits > 3 or digits < 2):
        return coordinates
    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])
    return degrees + "." + minutes
 
latitude = 0.0
longitude = 0.0
# Loop to read the analog input continuously
while True:
    print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
    time.sleep(0.2)

    
    data = gps.readline()
    data_str = data.decode('ascii')
    message = data[0:6]
    if (message == "$GPRMC"):
        parts = data.split(",")
        if parts[2] == "V":
            print("GPS receiver warning")
        else:
            longitude = float(formatDegreesMinutes(parts[5], 3))
            latitude = float(formatDegreesMinutes(parts[3], 2))
            print("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
    else:
        pass
