import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(16, GPIO.IN)  # Set GPIO4 as input

try:
    while True:
        vibration_detected = GPIO.input(16)
        if vibration_detected == 1:
            #print(1)  # Vibration detected
           print("value detected " + str(vibration_detected))
        elif vibration_detected == 0:
            print("value not detected " + str(vibration_detected))
        #    print(0)  # No vibration
        time.sleep(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    print("Exiting program")
    
finally:
    GPIO.cleanup()  # Clean up GPIO settings
