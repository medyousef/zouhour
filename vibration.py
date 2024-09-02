import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(16, GPIO.IN)  # Set GPIO16 as input
is_machine_on = False

try:
    detection_values = []
    start_time = time.time()

    while True:
        vibration_detected = GPIO.input(16)
        detection_values.append(vibration_detected)

        if time.time() - start_time >= 10:
            mean_value = sum(detection_values) / len(detection_values)
            print("Mean value detected: {:.2f}".format(mean_value))
            detection_values = []  # Reset the list
            start_time = time.time()  # Reset the timer
            if mean_value ==1 :
                is_machine_on = False
            else:
                is_machine_on = True
except KeyboardInterrupt:
    print("Exiting program")
    
finally:
    GPIO.cleanup()  # Clean up GPIO settings