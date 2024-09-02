import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(16, GPIO.IN)  # Set GPIO16 as input

try:
    detection_values = []
    start_time = time.time()

    while True:
        vibration_detected = GPIO.input(16)
        detection_values.append(vibration_detected)

        if time.time() - start_time >= 1:
            mean_value = sum(detection_values) / len(detection_values)
            print("Mean value detected: {:.2f}".format(mean_value))
            detection_values = []  # Reset the list
            start_time = time.time()  # Reset the timer

except KeyboardInterrupt:
    print("Exiting program")
    
finally:
    GPIO.cleanup()  # Clean up GPIO settings
