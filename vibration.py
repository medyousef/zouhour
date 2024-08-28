import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(4, GPIO.IN)  # Set GPIO4 as input

try:
    while True:
        vibration_detected = GPIO.input(4)
        if vibration_detected:
            print(1)  # Vibration detected
        else:
            print(0)  # No vibration
        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    print("Exiting program")
    
finally:
    GPIO.cleanup()  # Clean up GPIO settings
