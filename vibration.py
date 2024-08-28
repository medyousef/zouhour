import RPi.GPIO as GPIO
import time

# Set up GPIO
SENSOR_INPUT = 4  # GPIO4

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_INPUT, GPIO.IN)

try:
    while True:
        if GPIO.input(SENSOR_INPUT) == 0:
            print(1)  # Vibration detected
        else:
            print(0)  # No vibration
        time.sleep(0.5)  # Adjust the delay as needed

except KeyboardInterrupt:
    print("Exiting program")

finally:
    GPIO.cleanup()
