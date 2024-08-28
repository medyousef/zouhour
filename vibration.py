import RPi.GPIO as GPIO
import time

# Set up GPIO
SENSOR_INPUT = 4  # GPIO4
state = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_INPUT, GPIO.IN)

def vibration_detected(channel):
    global state
    state += 1
    print(f"Vibration detected! Count: {state}")

# Set up an interrupt to detect vibration on the falling edge
GPIO.add_event_detect(SENSOR_INPUT, GPIO.FALLING, callback=vibration_detected, bouncetime=500)

try:
    while True:
        time.sleep(0.1)  # Keep the program running

except KeyboardInterrupt:
    print("Exiting program")

finally:
    GPIO.cleanup()
